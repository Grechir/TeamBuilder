from django.urls import path
from .views import (ResponseList, ResponseDetail, ResponseCreate, ResponseDelete)

urlpatterns = [
    path('', ResponseList.as_view(), name='response-list'),
    path('<int:pk>/', ResponseDetail.as_view(), name='response-detail'),
    path('create/<int:post_id>/', ResponseCreate.as_view(), name='response-create'),
    path('<int:pk>/delete/', ResponseDelete.as_view(), name='response-delete'),
]
