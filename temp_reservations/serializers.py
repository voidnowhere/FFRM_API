from rest_framework import serializers

from users.models import User
from .models import Reservation, Field, FieldType


class AvailableFootBallFieldType(serializers.ModelSerializer):
    class Meta:
        model = FieldType
        fields = ('name',)


class AvailableFootBallFieldSerializer(serializers.ModelSerializer):
    type = AvailableFootBallFieldType()

    class Meta:
        model = Field
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


class ReservationsSerializer(serializers.ModelSerializer):
    field = AvailableFootBallFieldSerializer()
    date = serializers.DateField()
    begin_time = serializers.TimeField()
    end_time = serializers.TimeField()
    price_to_pay = serializers.IntegerField()
    is_paid = serializers.BooleanField()
    can_pay = serializers.BooleanField()

    class Meta:
        model = Reservation
        fields = ['id', 'date', 'begin_time', 'end_time', 'field', 'price_to_pay', 'is_paid', 'can_pay']


class UserPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


class ReservationPlayersSerializer(serializers.ModelSerializer):
    players = UserPlayerSerializer(many=True)

    class Meta:
        model = Reservation
        fields = ['players']


class PlayerEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UserIdSerializer(serializers.Serializer):
    id = serializers.UUIDField()
