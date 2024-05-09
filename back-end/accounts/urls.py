from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('<int:task_id>/', views.SearchView.as_view(), name='SearchView'),
]