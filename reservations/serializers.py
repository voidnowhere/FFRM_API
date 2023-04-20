from rest_framework import serializers

from .models import *


class FieldTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeField
        fields = ['name']


class FieldSerializer(serializers.ModelSerializer):
    type = FieldTypeSerializer()

    class Meta:
        model = Field
        fields = ['id', 'name', 'type', 'latitude', 'longitude']


class ReservationListSerializer(serializers.ModelSerializer):
    field = FieldSerializer()

    class Meta:
        model = Reservation
        fields = ['id', 'field', 'begin_date_time', 'end_date_time', 'is_public', 'price']


class ReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'field', 'begin_date_time', 'end_date_time']


class ReservationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['is_public']
