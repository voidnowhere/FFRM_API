from django.urls import path

from .views import ListCreateReservations, ReservationPlayersListAPIView, invite_player, remove_player, \
    AvailableReservationsListAPIView, join_reservation, update_public, delete_reservation

urlpatterns = [
    path('', ListCreateReservations.as_view()),
    path('<int:id>/update/', update_public),
    path('<int:id>/delete/', delete_reservation),
    path('<int:pk>/players/', ReservationPlayersListAPIView.as_view()),
    path('<int:pk>/players/invite/', invite_player),
    path('<int:pk>/players/remove/', remove_player),
    path('available/', AvailableReservationsListAPIView.as_view()),
    path('<int:pk>/join/', join_reservation),
]
