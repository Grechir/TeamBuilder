from django.urls import path
from .views import (NewsList)

urlpatterns = [
    path('', NewsList.as_view(), name='news-list'),
]
