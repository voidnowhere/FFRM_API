from rest_framework import serializers
from field_types.serializer import FieldTypeSerializer
from .models import Field


class FieldSerializer(serializers.ModelSerializer):
    type = FieldTypeSerializer()

    class Meta:
        model = Field
        fields = ['id', 'name', 'address', 'latitude', 'longitude', 'description', 'type', 'is_active', 'soil_type',
                  'zone', 'image']
        read_only_fields = ('id',)
