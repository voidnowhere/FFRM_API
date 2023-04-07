from datetime import datetime

from django.db.models import F, Count, Q, Exists, OuterRef, DateField, TimeField
from django.db.models.functions import Cast
from pytz import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from FFRM_API.settings import TIME_ZONE
from temp_reservations.models import Reservation
from temp_reservations.serializers import AvailableReservationsSerializer
from users.permissions import IsPlayer


class AvailableReservations(ListAPIView):
    serializer_class = AvailableReservationsSerializer
    permission_classes = [IsPlayer]

    def get_queryset(self):
        user = self.request.user
        return Reservation.objects.prefetch_related('field', 'field__type').annotate(
            available_places_excluding_owner=(
                    F('field__type__max') - Count('players', filter=~Q(players=user))
            ),
            available_places=F('field__type__max') - Count('players'),
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
