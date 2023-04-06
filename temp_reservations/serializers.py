from rest_framework import serializers

from temp_reservations.models import Reservation, FootBallField, FootBallFieldType


class AvailableFootBallFieldType(serializers.ModelSerializer):
    class Meta:
        model = FootBallFieldType
        fields = ('name',)


class AvailableFootBallFieldSerializer(serializers.ModelSerializer):
    type = AvailableFootBallFieldType()

    class Meta:
        model = FootBallField
        fields = ('name', 'type',)


class AvailableReservationsSerializer(serializers.ModelSerializer):
    field = AvailableFootBallFieldSerializer()
    available_places = serializers.IntegerField()
    is_joined = serializers.BooleanField()

    class Meta:
        model = Reservation
        fields = ('id', 'begin_date_time', 'end_date_dime', 'field', 'available_places', 'is_joined')
