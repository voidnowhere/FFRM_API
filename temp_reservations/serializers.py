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
    date = serializers.DateField()
    begin_time = serializers.TimeField()
    end_time = serializers.TimeField()
    available_places = serializers.IntegerField()
    is_joined = serializers.BooleanField()

    class Meta:
        model = Reservation
        fields = ('id', 'date', 'begin_time', 'end_time', 'field', 'available_places', 'is_joined',)
