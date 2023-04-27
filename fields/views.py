from fields.permissions import IsFieldOwner
from users.permissions import IsOwner
from .models import Field
from .serializers import FieldSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response


class FieldListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsOwner]
    serializer_class = FieldSerializer

    def get_queryset(self):
        return Field.objects.filter(type__in=self.request.user.field_types.all())

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        field = Field.objects.create(
            name=validated_data['name'],
            address=validated_data['address'],
            latitude=validated_data['latitude'],
            longitude=validated_data['longitude'],
            description=validated_data['description'],
            type=validated_data['type'],
            is_active=validated_data['is_active'],
            soil_type=validated_data['soil_type'],
            zone=validated_data['zone'],
            image=validated_data['image'],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class FieldRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwner, IsFieldOwner]
    serializer_class = FieldSerializer

    def get_queryset(self):
        return Field.objects.all()
