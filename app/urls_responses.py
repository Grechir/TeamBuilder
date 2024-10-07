from django.urls import path
from .views import (ResponseList, ResponseDetail)

urlpatterns = [
    path('', ResponseList.as_view(), name='response-list'),
    path('<int:pk>/', ResponseDetail.as_view(), name='response-create'),
]
