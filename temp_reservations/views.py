from datetime import datetime
from decimal import Decimal

import stripe
from django.db.models import F, Count, Q, Exists, OuterRef, DateField, TimeField, DecimalField, FloatField, \
    Subquery
from django.db.models.functions import Cast, Round, Now
from pytz import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from FFRM_API.settings import STRIPE_SECRET_KEY, TIME_ZONE, STRIPE_WEBHOOK_SIGNING_SECRET
from temp_reservations.models import Reservation, Payment
from temp_reservations.serializers import AvailableReservationsSerializer, ReservationsSerializer
from users.permissions import IsPlayer


class AvailableReservations(ListAPIView):
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
        available_places=F('field__type__max') - Count('players')
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


class Reservations(ListAPIView):
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
            can_pay=Q(begin_date_time__gte=datetime.now(timezone(TIME_ZONE))) and ~Exists(Subquery(
                Reservation.objects.exclude(pk=OuterRef('id')).filter(
                    begin_date_time__lte=OuterRef('end_date_time'),
                    end_date_time__gte=OuterRef('begin_date_time'),
                    field_id=OuterRef('field_id'),
                    payment__isnull=False,
                )
            ))
        ).filter(owner=self.request.user).order_by('begin_date_time')


@api_view(['GET'])
@permission_classes([IsPlayer])
def create_payment(request, pk):
    reservation = Reservation.objects.annotate(
        can_pay=Q(begin_date_time__gte=datetime.now(timezone(TIME_ZONE))) and ~Exists(Subquery(
            Reservation.objects.exclude(pk=OuterRef('id')).filter(
                begin_date_time__lte=OuterRef('end_date_time'),
                end_date_time__gte=OuterRef('begin_date_time'),
                field_id=OuterRef('field_id'),
                payment__isnull=False,
            )
        ))
    ).filter(pk=pk).first()
    if reservation is None:
        raise NotFound
    if reservation.owner_id != request.user.id:
        raise PermissionDenied
    if not reservation.can_pay:
        return Response({'message': 'Field already reserved at that time.'}, status=status.HTTP_400_BAD_REQUEST)
    if reservation.payment is not None:
        return Response(status=status.HTTP_403_FORBIDDEN)
    hours = (reservation.end_date_time - reservation.begin_date_time).total_seconds() / 3600
    amount_to_pay = Decimal(hours) * reservation.field.type.price_per_hour
    try:
        stripe.api_key = STRIPE_SECRET_KEY
        intent = stripe.PaymentIntent.create(
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
        print(e)
        return Response(status=status.HTTP_403_FORBIDDEN)


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
        reservation = Reservation.objects.filter(pk=int(payment_intent['metadata']['reservation_id'])).first()
        if reservation is not None and reservation.payment is None:
            reservation.payment = Payment.objects.create(
                pid=payment_intent['id'], created=datetime.fromtimestamp(payment_intent['created'])
            )
            reservation.save()
    # elif event['type'] == 'payment_method.attached':
    #     payment_method = event['data']['object']  # contains a stripe.PaymentMethod
    #     # Then define and call a method to handle the successful attachment of a PaymentMethod.
    #     # handle_payment_method_attached(payment_method)
    # else:
    #     # Unexpected event type
    #     print('Unhandled event type {}'.format(event['type']))

    return Response(status=status.HTTP_200_OK)
