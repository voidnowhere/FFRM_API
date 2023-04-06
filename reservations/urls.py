from django.contrib import admin
from django.urls import path, include
from . import views
from .views import ListCreateReservations, ReservationsUpdate

urlpatterns = [
    path('reservations/', ListCreateReservations.as_view()),
    path('reservations/<int:id>', ReservationsUpdate.as_view()),

]