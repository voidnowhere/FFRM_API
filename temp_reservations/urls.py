from django.urls import path

from temp_reservations.views import AvailableReservationsListAPIView, join_reservation, create_payment, \
    ReservationsListAPIView, payment_webhook, can_pay

urlpatterns = [
    path('', ReservationsListAPIView.as_view()),
    path('payment/webhook/', payment_webhook),
    path('<int:pk>/payment/', create_payment),
    path('<int:pk>/payment/can-pay', can_pay),
    path('available/', AvailableReservationsListAPIView.as_view()),
    path('<int:pk>/join/', join_reservation),
]
