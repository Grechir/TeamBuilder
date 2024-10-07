from django.urls import path
from .views import (PostList, PostDetail, PostCreate, PostUpdate, PostDelete)
from accounts.views import ConfirmUser

urlpatterns = [
    path('', PostList.as_view(), name='post-list'),
    path('<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('create/', PostCreate.as_view(), name='post-create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post-update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post-delete'),
    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
]
