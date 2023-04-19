from django.urls import path
from . import views

urlpatterns = [

    path('', views.FieldListCreateAPIView.as_view()),
    path('<int:pk>/', views.FieldRetrieveUpdateDestroyAPIView.as_view()),

    path('fieldtypes/', views.FieldTypeListCreateAPIView.as_view()),

    path('zones/', views.ZoneListAPIView.as_view()),
    path('zones/city=<int:city_id>/', views.ZoneByCityListAPIView.as_view()),
    path('zones/<int:pk>/city/', views.CityByZoneAPIView.as_view()),

    path('cities/', views.CityListAPIView.as_view()),
  
]
