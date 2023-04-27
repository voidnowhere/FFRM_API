from rest_framework import serializers

from field_types.models import FieldType
from fields.models import Field
from users.models import User
from .models import Reservation


class BookingDateTimeSerializer(serializers.Serializer):
    begin_date_time = serializers.DateTimeField()
    end_date_time = serializers.DateTimeField()


class BookingFieldTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldType
        fields = ['name']


class BookingFieldSerializer(serializers.ModelSerializer):
    type = BookingFieldTypeSerializer()

    class Meta:
        model = Field
        fields = ['id', 'name', 'type', 'image', 'latitude', 'longitude']


class FieldTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldType
        fields = ['name']


class FieldSerializer(serializers.ModelSerializer):
    type = FieldTypeSerializer()

    class Meta:
        model = Field
        fields = ['id', 'name', 'type', 'image', 'latitude', 'longitude']


class ReservationRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    field = FieldSerializer()

    class Meta:
        model = Reservation
        fields = ['id', 'field', 'begin_date_time', 'end_date_time', 'is_public', 'price_per_hour']


class ReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'field', 'begin_date_time', 'end_date_time']


class ReservationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['is_public']


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


class ReservationsListSerializer(serializers.ModelSerializer):
    field = AvailableFootBallFieldSerializer()
    date = serializers.DateField()
    begin_time = serializers.TimeField()
    end_time = serializers.TimeField()
    price_to_pay = serializers.IntegerField()
    is_paid = serializers.BooleanField()
    can_pay = serializers.BooleanField()

    class Meta:
        model = Reservation
        fields = ['id', 'date', 'begin_time', 'end_time', 'field', 'price_to_pay', 'is_public', 'is_paid', 'can_pay']


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
