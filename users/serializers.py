from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Player


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('email', 'password', 'nic', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        return Player.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            nic=validated_data['nic'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

    def update(self, instance, validated_data):
        if not check_password(validated_data.pop('password'), instance.password):
            raise serializers.ValidationError({'password': 'Current password is incorrect'})
        instance.email = validated_data.get('email', instance.email)
        instance.nic = validated_data.get('nic', instance.nic)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, max_length=128)
    new_password = serializers.CharField(required=True, max_length=128)
    confirmation = serializers.CharField(required=True, max_length=128)

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate_confirmation(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        if data.get('new_password') != data.get('confirmation'):
            raise serializers.ValidationError({'confirmation': 'New password and confirmation do not match'})
        return data
