from datetime import datetime

from django.db import models
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
            available_places=models.F('field__type__max') - models.Count('players', filter=~models.Q(players=user)),
            is_joined=models.Exists(
                Reservation.objects.filter(pk=models.OuterRef('id'), players=user)
            )
        ).filter(
            is_public=True,
            begin_date_time__gt=datetime.now(timezone(TIME_ZONE)),
            available_places__gt=0,
        )


@api_view(['PATCH'])
@permission_classes([IsPlayer])
def join_reservation(request, pk):
    reservation = Reservation.objects.annotate(
        available_places=models.F('field__type__max') - models.Count('players')
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
