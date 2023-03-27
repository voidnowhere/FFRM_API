from django.urls import path

from .views import register, Profile, update_password

urlpatterns = [
    path('register/', register, name="register"),
    path('profile/', Profile.as_view(), name="profile"),
    path('update_password/', update_password, name="update_password"),
]
