from django.urls import path
from . import views

urlpatterns = [

    path('', views.FieldListCreateAPIView.as_view()),
    path('add/', views.FieldListCreateAPIView.as_view()),
    path('update/<int:pk>/', views.FieldRetrieveUpdateDestroyAPIView.as_view()),
    path('delete/<int:pk>/', views.FieldRetrieveUpdateDestroyAPIView.as_view()),
    path('get/<int:pk>/', views.FieldRetrieveUpdateDestroyAPIView.as_view()),
    path('fieldtypes/', views.FieldTypeListCreateAPIView.as_view()),
    path('zones/', views.ZoneListCreateAPIView.as_view()),
    path('zones/city=<int:city_id>/', views.ZoneByCityAPIView.as_view()),
    path('cities/', views.CityListView.as_view()),
    path('zones/<int:pk>/city/', views.CityByZoneAPIView.as_view())
    # path('types/create/', views.TypeCreateAPIView.as_view()),
    # path('types/update/<int:pk>/', views.TypeUpdateAPIView.as_view()),
    # path('types/delete/<int:pk>/', views.TypeDestroyAPIView.as_view()),
    # path('types/get/<int:pk>/', views.TypeRetrieveAPIView.as_view()),
]
