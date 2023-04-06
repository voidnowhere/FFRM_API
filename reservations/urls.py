from django.contrib import admin
from django.urls import path, include
from . import views
from .views import ListCreateReservations, ReservationRetrieveUpdateDestroy

urlpatterns = [
    path('reservations/', ListCreateReservations.as_view()),
    path('reservations/<int:id>', ReservationRetrieveUpdateDestroy.as_view()),

]