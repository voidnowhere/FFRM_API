from django.urls import path
from .views import *

urlpatterns = [
    path('', FootBallFieldTypeView.as_view(), name='FootBallFieldTypeRecordView'),
    path('/<int:id>', FootBallFieldTypeView2.as_view(), name='FootBallFieldTypeRecordView')
]