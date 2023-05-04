from rest_framework import serializers

from field_types.models import FieldType
from fields.models import Field


class BookingDateTimeSerializer(serializers.Serializer):
    begin_date_time = serializers.DateTimeField()
    end_date_time = serializers.DateTimeField()
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)


class BookingFieldTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldType
        fields = ['name']


class BookingFieldSerializer(serializers.ModelSerializer):
    type = BookingFieldTypeSerializer()
    distance = serializers.FloatField(required=False)

    class Meta:
        model = Field
        fields = ['id', 'name', 'type', 'image', 'latitude', 'longitude', 'distance']
