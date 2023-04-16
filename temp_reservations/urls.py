from django.urls import path

from temp_reservations.views import AvailableReservations, join_reservation, create_payment, Reservations, \
    payment_webhook

urlpatterns = [
    path('', Reservations.as_view()),
    path('payment/webhook/', payment_webhook),
    path('<int:pk>/payment/', create_payment),
    path('available/', AvailableReservations.as_view()),
    path('<int:pk>/join/', join_reservation),
]
