from django.urls import path
from .views import TopProductsView

app_name = 'recommens'

urlpatterns = [
    path('api/top-products/', TopProductsView.as_view(), name='top-products'),
]