from datetime import datetime, time
from decimal import Decimal

import stripe
from django.db.models import F, Count, Q, Exists, OuterRef, DateField, TimeField, DecimalField, FloatField
from django.db.models.functions import Cast, Round, ExtractHour, ExtractMinute, ExtractSecond
from pytz import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from FFRM_API.settings import STRIPE_SECRET_KEY, TIME_ZONE, STRIPE_WEBHOOK_SIGNING_SECRET
from fields.models import Field
from users.models import User
from users.permissions import IsPlayer
from .models import Reservation, Payment
from .permissions import IsReservationOwner
from .serializers import FieldSerializer, ReservationsListSerializer, ReservationCreateSerializer, \
    ReservationRetrieveUpdateDestroySerializer, AvailableReservationsSerializer, ReservationPlayersSerializer, \
    PlayerEmailSerializer, UserIdSerializer


class FieldsListAPIView(ListAPIView):
    serializer_class = FieldSerializer
    queryset = Field.objects.all()


class ListCreateReservations(ListCreateAPIView):
    permission_classes = [IsPlayer]

    def get_queryset(self):
        return Reservation.objects.prefetch_related('field', 'field__type').annotate(
            date=Cast('begin_date_time', output_field=DateField()),
            begin_time=Cast('begin_date_time', output_field=TimeField()),
            end_time=Cast('end_date_time', output_field=TimeField()),
            date_diff=F('end_date_time') - F('begin_date_time'),
            duration=(
                    ExtractHour('date_diff', output_field=FloatField()) +
                    (ExtractMinute('date_diff', output_field=FloatField()) / 60) +
                    (ExtractSecond('date_diff', output_field=FloatField()) / 3600)
            ),
            price_to_pay=Round(
                Cast(F('duration'), output_field=DecimalField(max_digits=8, decimal_places=2)) *
                F('price_per_hour')
            ),
            is_paid=Q(payment__isnull=False),
            is_expired=Q(begin_date_time__lt=datetime.now(timezone(TIME_ZONE))),
            is_field_reserved=Exists(
                Reservation.objects.exclude(pk=OuterRef('id')).filter(
                    begin_date_time__lte=OuterRef('end_date_time'),
                    end_date_time__gte=OuterRef('begin_date_time'),
                    field_id=OuterRef('field_id'),
                    payment__isnull=False,
                )
            ),
            can_pay=Q(is_paid=False) and Q(is_field_reserved=False) and Q(is_expired=False)
        ).filter(owner=self.request.user).order_by('-begin_date_time')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReservationsListSerializer
        elif self.request.method == 'POST':
            return ReservationCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        #
        tz = timezone('UTC')

        # Check if begin_date_time is after now
        now = datetime.now(tz)
        if validated_data['begin_date_time'] <= now:
            return Response({'detail': 'Reservation must start after now.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the reservation is within the available range
        if Reservation.objects.filter(
                field=validated_data['field'],
                begin_date_time__lte=validated_data['end_date_time'],
                end_date_time__gte=validated_data['begin_date_time']
        ):
            return Response({'detail': 'Reservation is not available within the selected time range.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if validated_data['end_date_time'] <= validated_data['begin_date_time']:
            return Response({'detail': 'Reservation can not end before start.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if end_date_time is before midnight of the same day
        if validated_data['end_date_time'].date() != validated_data['begin_date_time'].date():
            return Response({'detail': 'Reservation can not end after midnight of the same day.'},
                            status=status.HTTP_400_BAD_REQUEST)
        elif validated_data['end_date_time'].time() >= time(hour=23, minute=59, second=59):
            return Response({'detail': 'Reservation can not end after midnight of the same day.'},
                            status=status.HTTP_400_BAD_REQUEST)

        duration = validated_data['end_date_time'] - validated_data['begin_date_time']

        reservation = Reservation.objects.create(
            field=validated_data['field'],
            begin_date_time=validated_data['begin_date_time'],
            end_date_time=validated_data['end_date_time'],
            price_per_hour=validated_data['field'].type.price_per_hour,
            owner=self.request.user
        )
        reservation.players.add(self.request.user)
        reservation.save()
        return Response(self.get_serializer(reservation).data)


class ReservationRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsPlayer, IsReservationOwner]
    serializer_class = ReservationRetrieveUpdateDestroySerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Reservation.objects.filter(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if reservation has already begun
        tz = timezone('UTC')
        now = datetime.now(tz)
        if instance.begin_date_time <= now:
            return Response({'detail': 'Reservation has already begun and cannot be deleted.'},
                            status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AvailableReservationsListAPIView(ListAPIView):
    serializer_class = AvailableReservationsSerializer
    permission_classes = [IsPlayer]

    def get_queryset(self):
        user = self.request.user
        return Reservation.objects.prefetch_related('field', 'field__type').annotate(
            available_places_excluding_owner=(
                    F('field__type__max_players') - Count('players', filter=~Q(players=user))
            ),
            available_places=F('field__type__max_players') - Count('players'),
            is_joined=Exists(
                Reservation.objects.filter(pk=OuterRef('id'), players=user)
            ),
            date=Cast('begin_date_time', output_field=DateField()),
            begin_time=Cast('begin_date_time', output_field=TimeField()),
            end_time=Cast('end_date_time', output_field=TimeField()),
        ).filter(
            is_public=True,
            begin_date_time__gt=datetime.now(timezone(TIME_ZONE)),
            available_places_excluding_owner__gt=0,
        ).order_by('-begin_date_time')


@api_view(['PATCH'])
@permission_classes([IsPlayer])
def join_reservation(request, pk):
    reservation = Reservation.objects.annotate(
        available_places=F('field__type__max_players') - Count('players')
    ).filter(pk=pk).first()
    if reservation is None:
        raise NotFound
    if reservation.available_places == 0:
        return Response({'message': 'Reservation is full.'}, status=status.HTTP_400_BAD_REQUEST)
    user = request.user
    if Reservation.objects.filter(pk=pk, players=user).exists():
        return Response({'message': 'You already joined this reservation.'}, status=status.HTTP_200_OK)
    reservation.players.add(user)
    return Response({'message': 'Joined reservation successfully.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsPlayer])
def create_payment(request, pk):
    reservation = Reservation.objects.annotate(
        is_paid=Q(payment__isnull=False),
        is_expired=Q(begin_date_time__lt=datetime.now(timezone(TIME_ZONE))),
        is_field_reserved=Exists(
            Reservation.objects.exclude(pk=OuterRef('id')).filter(
                begin_date_time__lte=OuterRef('end_date_time'),
                end_date_time__gte=OuterRef('begin_date_time'),
                field_id=OuterRef('field_id'),
                payment__isnull=False,
            )
        ),
        can_pay=Q(is_paid=False) and Q(is_field_reserved=False) and Q(is_expired=False)
    ).filter(pk=pk).first()
    if reservation is None:
        raise NotFound
    if reservation.owner_id != request.user.id:
        raise PermissionDenied
    if not reservation.can_pay:
        return Response({'message': 'Reservation is unavailable.'}, status=status.HTTP_400_BAD_REQUEST)
    hours = (reservation.end_date_time - reservation.begin_date_time).total_seconds() / 3600
    amount_to_pay = Decimal(hours) * reservation.field.type.price_per_hour
    try:
        intent = stripe.PaymentIntent.create(
            api_key=STRIPE_SECRET_KEY,
            amount=round(amount_to_pay) * 100,
            currency='mad',
            automatic_payment_methods={
                'enabled': True,
            },
            metadata={
                "reservation_id": reservation.id
            },
        )
        return Response({'client_secret': intent['client_secret']}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': 'Payment failed.'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsPlayer])
def can_pay(request, pk):
    reservation = Reservation.objects.annotate(
        is_paid=Q(payment__isnull=False),
        is_expired=Q(begin_date_time__lt=datetime.now(timezone(TIME_ZONE))),
        is_field_reserved=Exists(
            Reservation.objects.exclude(pk=OuterRef('id')).filter(
                begin_date_time__lte=OuterRef('end_date_time'),
                end_date_time__gte=OuterRef('begin_date_time'),
                field_id=OuterRef('field_id'),
                payment__isnull=False,
            )
        ),
        can_pay=Q(is_paid=False) and Q(is_field_reserved=False) and Q(is_expired=False)
    ).filter(pk=pk).first()
    if reservation is None:
        raise NotFound
    if reservation.owner_id != request.user.id:
        raise PermissionDenied
    if not reservation.can_pay:
        return Response({'message': 'Reservation is unavailable.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def payment_webhook(request):
    endpoint_secret = STRIPE_WEBHOOK_SIGNING_SECRET
    event = None
    payload = request.body

    if endpoint_secret:
        sig_header = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except stripe.error.SignatureVerificationError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    if event and event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
        if not payment_intent['metadata'].get('reservation_id', None):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        reservation = Reservation.objects.annotate(
            is_paid=Q(payment__isnull=False),
            is_expired=Q(begin_date_time__lt=datetime.now(timezone(TIME_ZONE))),
            is_field_reserved=Exists(
                Reservation.objects.exclude(pk=OuterRef('id')).filter(
                    begin_date_time__lte=OuterRef('end_date_time'),
                    end_date_time__gte=OuterRef('begin_date_time'),
                    field_id=OuterRef('field_id'),
                    payment__isnull=False,
                )
            ),
            can_pay=Q(is_paid=False) and Q(is_field_reserved=False) and Q(is_expired=False)
        ).filter(pk=int(payment_intent['metadata']['reservation_id'])).first()

        if reservation is not None and not hasattr(reservation, 'payment'):
            if not reservation.can_pay:
                stripe.Refund.create(
                    api_key=STRIPE_SECRET_KEY,
                    payment_intent=payment_intent['id'],
                )
            else:
                Payment.objects.create(
                    pid=payment_intent['id'],
                    created=datetime.fromtimestamp(payment_intent['created'], timezone(TIME_ZONE)),
                    reservation=reservation
                )

    return Response(status=status.HTTP_200_OK)


class ReservationPlayersListAPIView(RetrieveAPIView):
    serializer_class = ReservationPlayersSerializer
    permission_classes = [IsPlayer, IsReservationOwner]
    lookup_field = 'pk'

    def get_queryset(self):
        return Reservation.objects.all()


@api_view(['PATCH'])
@permission_classes([IsPlayer])
def invite_player(request, pk):
    email_serializer = PlayerEmailSerializer(data=request.data)
    email_serializer.is_valid(raise_exception=True)

    reservation = Reservation.objects.annotate(
        available_places=F('field__type__max_players') - Count('players')
    ).filter(pk=pk).first()
    if not reservation:
        raise NotFound
    if reservation.owner_id != request.user.id:
        raise PermissionDenied
    if datetime.now(timezone(TIME_ZONE)) > reservation.end_date_time:
        return Response({'message': "Reservation passed you can't invite player!"}, status=status.HTTP_400_BAD_REQUEST)
    if reservation.available_places == 0:
        return Response({'message': "Reservation is full!"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(email=email_serializer.validated_data['email'], type=User.PLAYER).first()
    if not user:
        return Response({'message': 'Player not found!'}, status=status.HTTP_400_BAD_REQUEST)
    if user in reservation.players.all():
        return Response({'message': 'Player already invited!'}, status=status.HTTP_400_BAD_REQUEST)

    reservation.players.add(user)
    return Response({'message': 'Player invited successfully.'}, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsPlayer])
def remove_player(request, pk):
    id_serializer = UserIdSerializer(data=request.data)
    id_serializer.is_valid(raise_exception=True)

    reservation = Reservation.objects.filter(pk=pk).first()
    if not reservation:
        raise NotFound
    if reservation.owner_id != request.user.id:
        raise PermissionDenied
    if datetime.now(timezone(TIME_ZONE)) > reservation.end_date_time:
        return Response({'message': "Reservation passed you can't remove player!"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.exclude(pk=request.user.id).filter(pk=id_serializer.validated_data['id']).first()
    if not user:
        return Response({'message': 'Player not found!'}, status=status.HTTP_400_BAD_REQUEST)

    reservation.players.remove(user)
    return Response({'message': 'Player removed successfully.'}, status=status.HTTP_200_OK)
