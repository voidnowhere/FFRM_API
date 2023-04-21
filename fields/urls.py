from django.urls import path

from .views import FieldListCreateAPIView, FieldRetrieveUpdateDestroyAPIView, FieldTypeListCreateAPIView, \
    ZoneListAPIView, ZoneByCityListAPIView, CityByZoneAPIView, CityListAPIView

urlpatterns = [
    path('', FieldListCreateAPIView.as_view()),
    path('<int:pk>/', FieldRetrieveUpdateDestroyAPIView.as_view()),
    path('fieldtypes/', FieldTypeListCreateAPIView.as_view()),
    path('zones/', ZoneListAPIView.as_view()),
    path('zones/city=<int:city_id>/', ZoneByCityListAPIView.as_view()),
    path('zones/<int:pk>/city/', CityByZoneAPIView.as_view()),
    path('cities/', CityListAPIView.as_view()),
]
