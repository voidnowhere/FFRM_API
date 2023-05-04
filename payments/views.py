from datetime import datetime
from decimal import Decimal

import stripe
from django.db.models import Q, Exists, OuterRef
from pytz import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response

from FFRM_API.settings import STRIPE_SECRET_KEY, TIME_ZONE, STRIPE_WEBHOOK_SIGNING_SECRET
from reservations.models import Reservation
from users.permissions import IsPlayer
from .models import Payment


@api_view(['GET'])
@permission_classes([IsPlayer])
def create_payment(request, reservation_id):
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
    ).filter(pk=reservation_id).first()
    if reservation is None:
        raise NotFound
    if reservation.owner_id != request.user.id:
        raise PermissionDenied
    if not reservation.can_pay:
        return Response({'message': 'Reservation is unavailable.'}, status=status.HTTP_400_BAD_REQUEST)
    total_seconds = (reservation.end_date_time - reservation.begin_date_time).total_seconds()
    amount_to_pay = Decimal(total_seconds) * (reservation.field.type.price_per_hour / 3600)
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
def can_pay(request, reservation_id):
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
    ).filter(pk=reservation_id).first()
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
