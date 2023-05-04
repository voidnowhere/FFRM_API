from django.urls import path

from .views import FieldListCreateAPIView, FieldRetrieveUpdateDestroyAPIView, get_paid_reservations

urlpatterns = [
    path('', FieldListCreateAPIView.as_view()),
    path('<int:pk>/', FieldRetrieveUpdateDestroyAPIView.as_view()),
    path('paid_reservations/', get_paid_reservations),
]
