from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from users.permissions import IsOwner
from .models import FootBallFieldType
from .permissions import IsFieldTypeOwner
from .serializer import *
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class FootBallFieldTypeListCreate(ListCreateAPIView):
    permission_classes = [IsOwner]
    serializer_class = FootBallFieldTypeSerializer

    def get_queryset(self):
        return FootBallFieldType.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        FootBallFieldType.objects.create(
            name=validated_data['name'],
            max=validated_data['max'],
            priceHour=validated_data['priceHour'],
            owner=self.request.user,
        )
        return Response({'message': ''}, status=status.HTTP_200_OK)


class FootBallFieldTypeRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwner, IsFieldTypeOwner]
    serializer_class = FootBallFieldTypeSerializer
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        return FootBallFieldType.objects.filter(owner=self.request.user)
