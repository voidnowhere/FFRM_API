from .models import Zone
from rest_framework.generics import ListAPIView,ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ZoneSerializer

class ZoneListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    
class ZoneByCityListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ZoneSerializer

    def get_queryset(self):
        city_id = self.kwargs['city_id']
        return Zone.objects.filter(city_id=city_id)


