from django.urls import path
from . import views

urlpatterns = [

    path('', views.ZoneListCreateAPIView.as_view()),
    path('city=<int:city_id>/', views.ZoneByCityListAPIView.as_view()),
   
  
]
