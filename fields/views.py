from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsOwner
from .models import Field,FieldType,Zone
from .serializers import FieldSerializer,ZoneSerializer,FieldTypeSerializer,CitySerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView,ListAPIView
from cities_light.models import City




class FieldListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsOwner]
    serializer_class = FieldSerializer

    def get_queryset(self):
        return Field.objects.filter(owner=self.request.user)
    # def get_queryset(self):
        # print(self.kwargs['zone_id'])
        # return Field.objects.filter(zone__id=self.kwargs['zone_id'])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        Field.objects.create(
            name=validated_data['name'],
            address=validated_data['address'],
            latitude=validated_data['latitude'],
            longitude=validated_data['longitude'],
            description=validated_data['description'],
            type=validated_data['type'],
            is_active=validated_data['is_active'],
            soil_type=validated_data['soil_type'],
            zone=validated_data['zone'],
            #image=validated_data['image'],
            owner=self.request.user,

        
        )
        return Response({'message': 'Field added successfully'}, status=status.HTTP_200_OK)

class FieldRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwner]
    serializer_class = FieldSerializer
    def get_queryset(self):
        return Field.objects.filter(owner=self.request.user)

class FieldTypeListCreateAPIView(ListCreateAPIView):
    queryset = FieldType.objects.all()
    serializer_class = FieldTypeSerializer
class ZoneListAPIView(ListAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    
class ZoneByCityListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ZoneSerializer

    def get_queryset(self):
        city_id = self.kwargs['city_id']
        return Zone.objects.filter(city_id=city_id)








class CityListAPIView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class CityByZoneAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CitySerializer
    queryset = City.objects.all()

    def get_object(self):
        zone_id = self.kwargs['pk']
        return City.objects.get(zone__id=zone_id)