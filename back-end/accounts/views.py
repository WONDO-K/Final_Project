from django.http import JsonResponse
from django.shortcuts import render
from .serializers import RegisterSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


from rest_framework.views import APIView 

# Create your views here.
# 회원가입
class RegisterView(APIView):
    
    @swagger_auto_schema(tags=['accounts'], request_body=RegisterSerializer) # swagger와 연동
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # jwt 토큰 접근
            token = TokenObtainPairSerializer().get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response({
                "user" : serializer.data,
                "message" : "regeistered successfully",
                "token" : {
                    "access" : access_token,
                    "refresh" : refresh_token,
                },
            }, status = status.HTTP_200_OK,
            ) 
            # 쿠키에 넣어주기
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)