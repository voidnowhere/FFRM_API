from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView,ListAPIView

class ZoneListAPIView(ListAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

    
class ZoneByCityListAPIView(ListAPIView):
    serializer_class = ZoneSerializer

    def get_queryset(self):
        city_id = self.kwargs['city_id']
        return Zone.objects.filter(city_id=city_id)

class FieldTypeListCreateAPIView(ListCreateAPIView):
    queryset = FieldType.objects.all()
    serializer_class = FieldTypeSerializer

class FieldListCreateAPIView(ListCreateAPIView):
    serializer_class = FieldSerializer
    queryset = Field.objects.all()
    # def get_queryset(self):
        # print(self.kwargs['zone_id'])
        # return Field.objects.filter(zone__id=self.kwargs['zone_id'])


class FieldRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer



class CityListView(ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class CityByZoneAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CitySerializer
    queryset = City.objects.all()

    def get_object(self):
        zone_id = self.kwargs['pk']
        return City.objects.get(zone__id=zone_id)