from django.urls import path
from .views import *

app_name = 'words'

urlpatterns = [
    path('web-crowler/', WebCrowlerAPIView.as_view(), name='web-crowler'),
    path('dictionary/', DictionaryAPIView.as_view(), name='dictionary'),
    path('cleanup/', CleanUpWordsAPIView.as_view(), name='cleanup'),
    path('list/', WordListAPIView.as_view(), name='list'),
    path('detail/<int:pk>/', WordDetailAPIView.as_view(), name='detail'),
]