from django.urls import path
from . import views

urlpatterns = [
    path('cities/all/', views.getCities),
    path('cities/add/', views.addCity),
    path('terrains/all/', views.getTerrains),
    path('terrains/add/', views.addTerrain),
    path('terrains/delete/<int:terrain_id>/', views.deleteTerrain),
    path('terrains/update/<int:pk>/', views.updateTerrain),
    path('types/all/', views.getTypes),
    path('types/add/', views.addType),
    path('types/delete/<int:type_id>/', views.deleteType),
    path('types/update/<int:pk>/', views.updateType)
]
