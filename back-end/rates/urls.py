from django.urls import path
from .views import RatesListAPIView

app_name = 'rates'

urlpatterns = [
    path('exchange-rate/', RatesListAPIView.as_view(), name='exchange-rate'),
]