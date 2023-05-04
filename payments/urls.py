from django.urls import path

from .views import payment_webhook, create_payment, can_pay

urlpatterns = [
    path('webhook/', payment_webhook),
    path('<int:reservation_id>/', create_payment),
    path('<int:reservation_id>/can-pay', can_pay),
]
