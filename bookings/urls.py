from django.urls import path

from .views import get_available_fields

urlpatterns = [
    path('fields/', get_available_fields),

]