from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from .models import FootBallFieldType
from .serializer import *


# Create your views here.

class FootBallFieldTypeListCreate(ListCreateAPIView):
    queryset = FootBallFieldType.objects.all()
    serializer_class = FootBallFieldTypeSerializer


class FootBallFieldTypeRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = FootBallFieldTypeSerializer
    lookup_url_kwarg = 'id'
    queryset = FootBallFieldType.objects.all()
