from datetime import datetime, time

import pytz
from rest_framework import status
from rest_framework.generics import *
from rest_framework.response import Response

from users.permissions import IsPlayer
from .permissions import IsReservationOwner
from .serializers import *


class ListCreateReservations(ListCreateAPIView):
    permission_classes = [IsPlayer]

    def get_queryset(self):
        return Reservation.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReservationListSerializer
        elif self.request.method == 'POST':
            return ReservationCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        #
        tz = pytz.timezone('UTC')

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
        duration_hours = duration.total_seconds() / 3600.0

        reservation = Reservation.objects.create(
            field=validated_data['field'],
            begin_date_time=validated_data['begin_date_time'],
            end_date_time=validated_data['end_date_time'],
            price=validated_data['field'].type.price * duration_hours,
            owner=self.request.user
        )
        reservation.players.add(self.request.user)
        reservation.save()
        return Response(self.get_serializer(reservation).data)


class ReservationRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsPlayer, IsReservationOwner]
    serializer_class = ReservationListSerializer
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ReservationUpdateSerializer
        return ReservationListSerializer

    def get_queryset(self):
        return Reservation.objects.filter(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



