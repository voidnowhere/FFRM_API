from django.urls import path
from . import views

urlpatterns = [

    path('', views.CityListAPIView.as_view()),
    path('<int:pk>/city/', views.CityByZoneAPIView.as_view()),
 
]
