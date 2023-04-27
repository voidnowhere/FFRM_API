from django.urls import path

from .views import ListCreateReservations, ReservationRetrieveUpdateDestroy, \
    ReservationPlayersListAPIView, invite_player, remove_player, payment_webhook, create_payment, can_pay, \
    AvailableReservationsListAPIView, join_reservation, get_available_fields

urlpatterns = [
    path('', ListCreateReservations.as_view()),
    path('fields/', get_available_fields),
    path('<int:id>/', ReservationRetrieveUpdateDestroy.as_view()),
    path('<int:pk>/players/', ReservationPlayersListAPIView.as_view()),
    path('<int:pk>/players/invite/', invite_player),
    path('<int:pk>/players/remove/', remove_player),
    path('payment/webhook/', payment_webhook),
    path('<int:pk>/payment/', create_payment),
    path('<int:pk>/payment/can-pay', can_pay),
    path('available/', AvailableReservationsListAPIView.as_view()),
    path('<int:pk>/join/', join_reservation),
]
