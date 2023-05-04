from datetime import datetime

from django.db.models import Exists, OuterRef, F
from django.db.models.functions import Radians, Sin, Cos, ATan2, Sqrt
from pytz import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from FFRM_API.settings import TIME_ZONE
from fields.models import Field
from reservations.models import Reservation
from .serializers import BookingDateTimeSerializer, BookingFieldSerializer


# Create your views here.

@api_view(['POST'])
def get_available_fields(request):
    serializer = BookingDateTimeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    begin_date_time = serializer.validated_data['begin_date_time']
    end_date_time = serializer.validated_data['end_date_time']
    latitude = serializer.validated_data['latitude']
    longitude = serializer.validated_data['longitude']
    date_time_now = datetime.now(timezone(TIME_ZONE))

    if date_time_now < begin_date_time < end_date_time:
        if latitude and longitude:
            fields = Field.objects.annotate(
                is_booked=Exists(
                    Reservation.objects.filter(
                        field_id=OuterRef('id'),
                        begin_date_time__lte=end_date_time,
                        end_date_time__gte=begin_date_time,
                        payment__isnull=False
                    )
                ),
                p1=Radians('latitude'),
                p2=Radians(latitude),
                d1=Radians(latitude - F('latitude')),
                d2=Radians(longitude - F('longitude')),
                a=Sin(F('d1') / 2) * Sin(F('d1') / 2) + Cos(F('p1')) * Cos(F('p2')) * Sin(F('d2') / 2) * Sin(
                    F('d2') / 2),
                c=2 * ATan2(Sqrt(F('a')), Sqrt(1 - F('a'))),
                distance=6371 * F('c'),
            ).filter(is_booked=False, is_active=True).order_by('distance')
            return Response(BookingFieldSerializer(fields, many=True, context={'request': request}).data,
                            status=status.HTTP_200_OK)

        else:
            fields = Field.objects.annotate(
                is_booked=Exists(
                    Reservation.objects.filter(
                        field_id=OuterRef('id'),
                        begin_date_time__lte=end_date_time,
                        end_date_time__gte=begin_date_time,
                        payment__isnull=False
                    )
                )
            ).filter(is_booked=False, is_active=True)
            return Response(BookingFieldSerializer(fields, many=True, context={'request': request}).data,
                            status=status.HTTP_200_OK)

    else:
        return Response({'detail': 'Invalid Reservation date and time.'},
                        status=status.HTTP_400_BAD_REQUEST)
