from _decimal import Decimal
from rest_framework import serializers

from field_types.models import FieldType
from fields.models import Field
from users.models import User
from .models import Reservation
from fields.serializers import NestedFieldSerializer
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


class FieldOwnerReservationSerializer(serializers.ModelSerializer):
    owner = UserPlayerSerializer()
    total_amount = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    begin_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()
    field = NestedFieldSerializer()
    players_count = serializers.SerializerMethodField()

    def get_date(self, obj):
        return obj.begin_date_time.date()

    def get_begin_time(self, obj):
        return obj.begin_date_time.time()

    def get_end_time(self, obj):
        return obj.end_date_time.time()

    def get_owner(self, obj):
        return obj.owner

    def get_total_amount(self, obj):
        field_type_price = obj.field.type.price_per_hour
        duration = Decimal((obj.end_date_time - obj.begin_date_time).total_seconds()) / Decimal(3600)
        total_amount = field_type_price * duration
        return total_amount

    def get_players_count(self, obj):
        return obj.players.count()

    class Meta:
        model = Reservation
        fields = ['id', 'date', 'begin_time', 'end_time',
                  'total_amount', 'field',
                  'owner', 'players', 'players_count']
