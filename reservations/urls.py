from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('reservations/', views.getReservation),
    path('reservations/add/', views.addResrvation),
    path('reservations/<int:pk>/cancel/', views.cancelReservation),

]