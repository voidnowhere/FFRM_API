from django.urls import path
from .views import *

urlpatterns = [
    path('', FootBallFieldTypeRecordView.as_view(), name='FootBallFieldTypeRecordView'),
    path('/<int:id>', FootBallFieldTypeRecordView.as_view(), name='FootBallFieldTypeRecordView')
]