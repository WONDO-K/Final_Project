from django.urls import path,re_path
from .views import RegisterView
from django.contrib import admin

app_name = 'accounts'

urlpatterns = [
    # 회원가입하기
    re_path('admin/', admin.site.urls),
    re_path("register/", RegisterView.as_view(), name='register'), 
]
