from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FootBallFieldType
from .serializer import *

# Create your views here.

class FootBallFieldTypeRecordView(APIView):

    def get(self, request, format=None, id =None):
        if id:
            item = FootBallFieldType.objects.get(id=id)
            serializer = FootBallFieldTypeSerializer(item)
            return Response(serializer.data)
        footBallFieldType = FootBallFieldType.objects.all()
        serializer = FootBallFieldTypeSerializer(footBallFieldType, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FootBallFieldTypeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id = None):
        item = FootBallFieldType.objects.get(id=id)
        serializer = FootBallFieldTypeSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id =None):
        item = get_object_or_404(FootBallFieldType, id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})

