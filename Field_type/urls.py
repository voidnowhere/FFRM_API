from django.urls import path
from .views import *

urlpatterns = [
    path('', FootBallFieldTypeListCreate.as_view(), name='FootBallFieldTypeRecordView'),
    path('/<int:id>', FootBallFieldTypeRetrieveUpdateDestroy.as_view(), name='FootBallFieldTypeRecordView')
]