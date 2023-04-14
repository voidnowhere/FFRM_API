from django.urls import path
from . import views

urlpatterns = [

    path('', views.FieldListCreateAPIView.as_view()),
    path('fieldtypes/', views.FieldTypeListCreateAPIView.as_view()),
    path('zones/', views.ZoneListAPIView.as_view()),
    path('zones/city=<int:city_id>/', views.ZoneByCityListAPIView.as_view()),
    path('cities/', views.CityListView.as_view()),
    path('zones/<int:pk>/city/', views.CityByZoneAPIView.as_view())
    # path('types/create/', views.TypeCreateAPIView.as_view()),
    # path('types/update/<int:pk>/', views.TypeUpdateAPIView.as_view()),
    # path('types/delete/<int:pk>/', views.TypeDestroyAPIView.as_view()),
    # path('types/get/<int:pk>/', views.TypeRetrieveAPIView.as_view()),
]
