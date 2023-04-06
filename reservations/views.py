from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import *
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import *


class ListCreateReservations(ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        # get the field and begin_date_time from the request data
        field_id = request.data.get('field')
        begin_hour = request.data.get('begin_date_time')
        end_hour = request.data.get('end_date_time')

        # check if there is a reservation with the same field and time range
        existing_reservations = Reservation.objects.filter(
            field=field_id, begin_date_time__lte=end_hour, end_date_time__gte=begin_hour
        )
        if existing_reservations.exists():
            return Response(
                {'error': 'A reservation already exists for this field and time range.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # create the reservation
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ReservationRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # check if the updated reservation conflicts with an existing reservation
        field_id = request.data.get('field') or instance.field_id
        begin_hour = request.data.get('begin_date_time') or instance.begin_date_time
        end_hour = request.data.get('end_date_time') or instance.end_date_time
        existing_reservation = Reservation.objects.exclude(id=instance.id).filter(field=field_id, begin_date_time__lte=end_hour, end_date_time__gte=begin_hour).first()
        if existing_reservation:
            return Response({'error': 'A reservation already exists for this field and time.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # update the reservation
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        reservation = self.get_object()
        if reservation.isPaid:
            return Response({'error': 'Paid reservations cannot be deleted.'},
                            status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(reservation)
        return Response(status=status.HTTP_204_NO_CONTENT)

