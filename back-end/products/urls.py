from django.urls import path
from .views import *

app_name = 'products'

urlpatterns = [
    path('banks/', BankRegisterAPIView.as_view(), name='bank-register'),
    path('banks/<int:bank_pk>/', BankDetailAPIView.as_view(), name='bank-detail'),
    path('deposit/register/', DepositProductRegisterAPIView.as_view(), name='product-register'),
    path('deposit/<int:product_pk>/', DepositProductDetailAPIView.as_view(), name='product-detail'),
]