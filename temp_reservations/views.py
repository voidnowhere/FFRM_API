from datetime import datetime
from decimal import Decimal

import stripe
from django.db.models import F, Count, Q, Exists, OuterRef, DateField, TimeField, DecimalField, FloatField
from django.db.models.functions import Cast, Round
from pytz import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from FFRM_API.settings import STRIPE_SECRET_KEY, TIME_ZONE, STRIPE_WEBHOOK_SIGNING_SECRET
from temp_reservations.models import Reservation, Payment
from temp_reservations.permissions import IsReservationOwner
from temp_reservations.serializers import AvailableReservationsSerializer, ReservationsSerializer, \
    ReservationPlayersSerializer, PlayerEmailSerializer, UserIdSerializer
from users.models import User
from users.permissions import IsPlayer


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
        ).order_by('begin_date_time')


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


class ReservationsListAPIView(ListAPIView):
    serializer_class = ReservationsSerializer
    permission_classes = [IsPlayer]

    def get_queryset(self):
        return Reservation.objects.prefetch_related('field', 'field__type').annotate(
            date=Cast('begin_date_time', output_field=DateField()),
            begin_time=Cast('begin_date_time', output_field=TimeField()),
            end_time=Cast('end_date_time', output_field=TimeField()),
            duration_hours=Cast(F('end_time') - F('begin_time'), output_field=FloatField()) / (3600 * 10 ** 6),
            price_to_pay=Round(
                Cast(F('duration_hours'), output_field=DecimalField()) * F('field__type__price_per_hour')
            ),
            is_paid=Q(payment__isnull=False),
            can_pay=Q(begin_date_time__gte=datetime.now(timezone(TIME_ZONE))) and Q(payment__isnull=True) and ~Exists(
                Reservation.objects.exclude(pk=OuterRef('id')).filter(
                    begin_date_time__lte=OuterRef('end_date_time'),
                    end_date_time__gte=OuterRef('begin_date_time'),
                    field_id=OuterRef('field_id'),
                    payment__isnull=False,
                )
            )
        ).filter(owner=self.request.user).order_by('begin_date_time')


@api_view(['GET'])
@permission_classes([IsPlayer])
def create_payment(request, pk):
    reservation = Reservation.objects.annotate(
        can_pay=Q(begin_date_time__gte=datetime.now(timezone(TIME_ZONE))) and Q(payment__isnull=True) and ~Exists(
            Reservation.objects.filter(
                begin_date_time__lte=OuterRef('end_date_time'),
                end_date_time__gte=OuterRef('begin_date_time'),
                field_id=OuterRef('field_id'),
                payment__isnull=False,
            )
        )
    ).filter(pk=pk).first()
    if reservation is None:
        raise NotFound
    if reservation.owner_id != request.user.id:
        raise PermissionDenied
    if not reservation.can_pay:
        return Response({'message': 'Field already reserved at that time.'}, status=status.HTTP_400_BAD_REQUEST)
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
        can_pay=Q(begin_date_time__gte=datetime.now(timezone(TIME_ZONE))) and Q(payment__isnull=True) and ~Exists(
            Reservation.objects.filter(
                begin_date_time__lte=OuterRef('end_date_time'),
                end_date_time__gte=OuterRef('begin_date_time'),
                field_id=OuterRef('field_id'),
                payment__isnull=False,
            )
        )
    ).filter(pk=pk).first()
    if reservation is None:
        raise NotFound
    if reservation.owner_id != request.user.id:
        raise PermissionDenied
    if not reservation.can_pay:
        return Response({'message': 'Field already reserved at that time.'}, status=status.HTTP_400_BAD_REQUEST)
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
            can_pay=Q(begin_date_time__gte=datetime.now(timezone(TIME_ZONE))) and Q(payment__isnull=True) and ~Exists(
                Reservation.objects.filter(
                    begin_date_time__lte=OuterRef('end_date_time'),
                    end_date_time__gte=OuterRef('begin_date_time'),
                    field_id=OuterRef('field_id'),
                    payment__isnull=False,
                )
            )
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

    user = User.objects.filter(email=email_serializer.validated_data['email']).first()
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

    user = User.objects.filter(pk=id_serializer.validated_data['id']).first()
    if not user:
        return Response({'message': 'Player not found!'}, status=status.HTTP_400_BAD_REQUEST)

    reservation.players.remove(user)
    return Response({'message': 'Player removed successfully.'}, status=status.HTTP_200_OK)
