from django.urls import path
from .views import *

app_name = 'words'

urlpatterns = [
    path('register/', WordProcessingAPIView.as_view(), name='register'),
    path('random/', randomWordAPIView.as_view(), name='random'),
]