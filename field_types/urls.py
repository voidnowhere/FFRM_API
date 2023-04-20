from django.urls import path
from .views import *

urlpatterns = [
    path('', FootBallFieldTypeListCreate.as_view(), name='FootBallFieldTypeListCreate'),
    path('<int:id>/', FootBallFieldTypeRetrieveUpdateDestroy.as_view(), name='FootBallFieldTypeRetrieveUpdateDestroy'),
]