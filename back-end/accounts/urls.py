from django.urls import path,re_path
from .views import *
from django.contrib import admin
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers

app_name = 'accounts'

urlpatterns = [
    # 회원가입하기
    re_path('admin/', admin.site.urls),
    re_path("register/", RegisterAPIView.as_view(), name='register'), 
    re_path("auth/", AuthAPIView.as_view(), name='auth'),
]
