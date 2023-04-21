from .models import City
from .serializers import CitySerializer
from rest_framework.generics import  RetrieveUpdateDestroyAPIView,ListAPIView

class CityListAPIView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class CityByZoneAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CitySerializer
    queryset = City.objects.all()

    def get_object(self):
        zone_id = self.kwargs['pk']
        return City.objects.get(zone__id=zone_id)