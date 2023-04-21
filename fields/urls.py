from django.urls import path
from . import views

urlpatterns = [

    path('', views.FieldListCreateAPIView.as_view()),
    path('<int:pk>/', views.FieldRetrieveUpdateDestroyAPIView.as_view()),
  
]
