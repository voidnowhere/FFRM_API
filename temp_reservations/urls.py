from django.urls import path

from temp_reservations.views import AvailableReservationsListAPIView, join_reservation, create_payment, \
    ReservationsListAPIView, payment_webhook, can_pay, ReservationPlayersListAPIView, invite_player, remove_player

urlpatterns = [
    path('', ReservationsListAPIView.as_view()),
    path('<int:pk>/players/', ReservationPlayersListAPIView.as_view()),
    path('<int:pk>/players/invite/', invite_player),
    path('<int:pk>/players/remove/', remove_player),
    path('payment/webhook/', payment_webhook),
    path('<int:pk>/payment/', create_payment),
    path('<int:pk>/payment/can-pay', can_pay),
    path('available/', AvailableReservationsListAPIView.as_view()),
    path('<int:pk>/join/', join_reservation),
]
