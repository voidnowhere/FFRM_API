from django.urls import path
from . import views

urlpatterns = [
    path('cities/all/', views.getCities),
    path('cities/add/', views.addCity),
    path('', views.FieldListAPIView.as_view()),
    path('create/', views.FieldCreateAPIView.as_view()),
    path('update/<int:pk>/', views.FieldUpdateAPIView.as_view()),
    path('delete/<int:pk>/', views.FieldDestroyAPIView.as_view()),
    path('get/<int:pk>/', views.FieldRetrieveAPIView.as_view()),
    path('types/', views.TypeListAPIView.as_view()),
    path('types/create/', views.TypeCreateAPIView.as_view()),
    path('types/update/<int:pk>/', views.TypeUpdateAPIView.as_view()),
    path('types/delete/<int:pk>/', views.TypeDestroyAPIView.as_view()),
    path('types/get/<int:pk>/', views.TypeRetrieveAPIView.as_view()),
    
]
