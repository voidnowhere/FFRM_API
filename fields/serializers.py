from rest_framework import serializers
from .models import Field



class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ['id','name','address','latitude','longitude','description','type','is_active','soil_type','zone']
        read_only_fields = ('id',)


