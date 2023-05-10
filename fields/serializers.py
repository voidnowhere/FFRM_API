from rest_framework import serializers

from field_types.models import FieldType
from .models import Field


class FieldTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldType
        fields = ['id', 'name', 'max_players', 'price_per_hour']


class FieldSerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(
        queryset=FieldType.objects.all()
    )

    class Meta:
        model = Field
        fields = ['id', 'name', 'address', 'latitude', 'longitude', 'description', 'type', 'is_active', 'soil_type',
                  'zone', 'image']
        read_only_fields = ('id',)


class NestedFieldSerializer(serializers.ModelSerializer):
    type = FieldTypeSerializer(many=False)

    class Meta:
        model = Field
        fields = ['id', 'name', 'address', 'latitude', 'longitude', 'description', 'type', 'is_active', 'soil_type',
                  'zone', 'image']
        read_only_fields = ('id',)
