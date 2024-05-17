from django.urls import path
from .views import RatesListAPIView, ExchangeMoneyAPIView

app_name = 'rates'

urlpatterns = [
    path('exchange-rate/', RatesListAPIView.as_view(), name='exchange-rate'),
    path('convert/', ExchangeMoneyAPIView.as_view(), name='exchange-money'),
]