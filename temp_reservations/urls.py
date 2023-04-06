from django.urls import path

from temp_reservations.views import AvailableReservations, join_reservation

urlpatterns = [
    path('available/', AvailableReservations.as_view()),
    path('<int:pk>/join/', join_reservation),
]
