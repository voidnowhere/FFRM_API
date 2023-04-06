from rest_framework import serializers, status
from .models import *


class FootBallFieldTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FootBallFieldType
        fields = ('id', 'name', 'max', 'price', 'advance',)
