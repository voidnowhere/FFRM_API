from rest_framework import serializers
from .models import City

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id','name']
        read_only_fields = ('id',)
