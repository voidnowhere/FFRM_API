from django.urls import path

from .views import FieldListCreateAPIView, FieldRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', FieldListCreateAPIView.as_view()),
    path('<int:pk>/', FieldRetrieveUpdateDestroyAPIView.as_view()),
]
