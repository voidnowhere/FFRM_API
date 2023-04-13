from datetime import datetime

from rest_framework import status
from rest_framework.generics import *
from rest_framework.response import Response

from .serializers import *


class ListCreateReservations(ListCreateAPIView):
    queryset = Reservation.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReservationListSerializer
        elif self.request.method == 'POST':
            return ReservationCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        validated_data = serializer.validated_data
        #
        reservation = Reservation.objects.create(
            field=validated_data['field'],
            begin_date_time=validated_data['begin_date_time'],
            end_date_time=validated_data['end_date_time'],
            price=validated_data['field'].type.price,
            owner_id=1
        )
        return Response(self.get_serializer(reservation).data)


class ReservationRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationListSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # check if the updated reservation conflicts with an existing reservation
        field_id = request.data.get('field')
        begin_hour = datetime.strptime(request.data.get('begin_date_time'), '%Y-%m-%dT%H:%M')
        end_hour = datetime.strptime(request.data.get('end_date_time'), '%Y-%m-%dT%H:%M')
        # if begin_hour < datetime.now():
        #     return Response(
        #         {'error': 'Reservation start time cannot be in the past.'},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        # if end_hour.date() != begin_hour.date() or end_hour.time() > time(00, 00):
        #     return Response(
        #         {'error': 'Reservation end time must be on the same day and before 00:00.'},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        # Check if there is a reservation with the same field and time range
        existing_reservation = Reservation.objects.exclude(id=instance.id).filter(
            field=field_id, begin_date_time__lte=end_hour, end_date_time__gte=begin_hour
        ).first()
        if existing_reservation:
            return Response({'error': 'A reservation already exists for this field and time.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Update the reservation
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
