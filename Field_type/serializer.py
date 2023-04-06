from rest_framework import serializers, status
from .models import *


class FootBallFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FootBallField
        fields = ('id', 'name',)

    def create(self, validated_data):
        return FootBallField.objects.create(
            name=validated_data['name'],

        )


class FootBallFieldTypeSerializer(serializers.ModelSerializer):
    footBallField = FootBallFieldSerializer(required=True)

    class Meta:
        model = FootBallFieldType
        fields = ('id', 'name', 'max', 'price', 'advance', 'footBallField',)

    
