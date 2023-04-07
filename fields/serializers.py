from rest_framework import serializers
from .models import *
import re

class FieldSerializer(serializers.ModelSerializer):
    address = serializers.CharField(max_length=255, required=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    type = serializers.PrimaryKeyRelatedField(queryset=Type.objects.all(), required=True)
    zone = serializers.PrimaryKeyRelatedField(queryset=Zone.objects.all(), required=True)
    soil_type = serializers.ChoiceField(choices=Field.TYPE_CHOICES2, required=True)

    class Meta:
        model = Field
        fields = '__all__'
        read_only_fields = ('id',)

    def validate_name(self, value):
        if not re.match(r'^[a-zA-Z ]+$', value):
            raise serializers.ValidationError('Name field can only contain letters and spaces.')
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('Price field must be positive.')
        return value

    def validate_address(self, value):
        if not value:
            raise serializers.ValidationError('Address field cannot be empty.')
        return value

    def validate_type(self, value):
        if not value:
            raise serializers.ValidationError('Type field cannot be empty.')
        return value

    def validate_zone(self, value):
        if not value:
            raise serializers.ValidationError('Zone field cannot be empty.')
        return value

    def validate_soil_type(self, value):
        if not value:
            raise serializers.ValidationError('Soil type field cannot be empty.')
        return value


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'
        read_only_fields = ('id',)


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = '__all__'
        read_only_fields = ('id',)


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'
        read_only_fields = ('id',)
