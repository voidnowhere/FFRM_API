from rest_framework import serializers
from .models import *


class FieldSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Field
        fields = ['id','name','address','latitude','longitude','description','field_type','is_active','soil_type','zone']
        read_only_fields = ('id',)


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ['id','name']
        read_only_fields = ('id',)


class FieldTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldType
        fields = ['id','name']
        read_only_fields = ('id',)

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id','name']
        read_only_fields = ('id',)
