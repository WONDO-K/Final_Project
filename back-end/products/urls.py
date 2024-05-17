from django.urls import path
from .views import *

app_name = 'products'

urlpatterns = [
    path('banks/', BankListAPIView.as_view(), name='bank-list'),
    path('banks/<int:bank_pk>/', BankDetailAPIView.as_view(), name='bank-detail'),
]