from django.urls import path
from .views import NewsSearchAPIView

app_name = 'news'

urlpatterns = [
    path('search/', NewsSearchAPIView.as_view(), name='news_search'),
]