from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    # 회원가입하기

    path("register/", RegisterAPIView.as_view(), name='register'), 
    path("auth/", AuthAPIView.as_view(), name='auth'),
    path("update/", UserRetrieveUpdateAPIView.as_view(), name='update'),
    path("change_pasword/", ChangePasswordAPIView.as_view(), name='change_pasword'),
]
