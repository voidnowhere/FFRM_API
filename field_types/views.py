from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from users.permissions import IsOwner
from .models import FieldType
from .permissions import IsFieldTypeOwner
from .serializer import FieldTypeSerializer


# Create your views here.

class FootBallFieldTypeListCreate(ListCreateAPIView):
    permission_classes = [IsOwner]
    serializer_class = FieldTypeSerializer

    def get_queryset(self):
        return FieldType.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        FieldType.objects.create(
            name=validated_data['name'],
            max_players=validated_data['max_players'],
            price_per_hour=validated_data['price_per_hour'],
            owner=self.request.user,
        )
        return Response({'message': ''}, status=status.HTTP_200_OK)


class FootBallFieldTypeRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwner, IsFieldTypeOwner]
    serializer_class = FieldTypeSerializer
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        return FieldType.objects.all()
