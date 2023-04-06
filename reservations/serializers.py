from rest_framework import serializers
from .models import *



class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'field', 'begin_date_time', 'end_date_time', 'isPaid', 'player']
