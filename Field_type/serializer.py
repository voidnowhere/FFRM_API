from rest_framework import serializers, status
from .models import *


class FootBallFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FootBallField
        fields = '__all__'

    def create(self, validated_data):
        return FootBallField.objects.create(
            name=validated_data['name'],

        )


class FootBallFieldTypeSerializer(serializers.ModelSerializer):
    footBallField = FootBallFieldSerializer(required=True)

    class Meta:
        model = FootBallFieldType
        fields = '__all__'

    def create(self, validated_data):
        footBallField_data = validated_data.pop('footBallField')
        footBallField = FootBallFieldSerializer.create(FootBallFieldSerializer(), validated_data=footBallField_data)
        footBallfield, created = FootBallFieldType.objects.update_or_create(footBallField=footBallField,
                                                                            name=validated_data.pop('name'),
                                                                            max=validated_data.pop('max'),
                                                                            price=validated_data.pop('price'),
                                                                            advance=validated_data.pop('advance'))
        return footBallfield
