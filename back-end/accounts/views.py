import jwt
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404, render
from .serializers import *
from rest_framework_simplejwt.serializers import *
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.renderers import JSONRenderer
#from rest_framework.parsers import JSONParser


from rest_framework.views import APIView 

# Create your views here.
# 회원가입
class RegisterAPIView(APIView):
    @swagger_auto_schema(tags=['회원가입'], request_body=UserSerializer) # swagger와 연동
    def post(self, request):
        serializer = UserSerializer(data=request.data)
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

# 로그인 및 인증
class AuthAPIView(APIView):
    # 유저 정보 가져오기
    @swagger_auto_schema(tags=['로그인 및 인증'])
    def get(self, request):
        try:
            # access token을 decode 해서 유저 id 추출 => 유저 식별
            access = request.COOKIES.get('access')
            payload = jwt.decode(access, settings.SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료시 토큰 갱신
            data = {'refresh' : request.COOKIES.get('refresh',None)}
            serializer = TokenRefreshSerializer(data=data) # TokenRefreshSerializer가 refresh token을 받아서 access token을 재발급해준다.
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access',None)
                refresh = serializer.data.get('refresh',None)
                payload = jwt.decode(access, settings.SECRET_KEY, algorithms=['HS256']) # access token을 HS256로 decode하여 payload를 가져온다. 여기서 payload란 토큰에 담긴 정보를 말한다.
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)
                serializer = UserSerializer(instance=user)
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie("access", access)
                res.set_cookie("refresh", refresh)
                return res
            raise jwt.exceptions.InvalidTokenError
        except (jwt.exceptions.InvalidTokenError):
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # 로그인
    @swagger_auto_schema(tags=['로그인 및 인증'], request_body=LoginSerializer) # swagger와 연동
    def post(self,request):
        user = authenticate(
            username=request.data.get('username'), 
            password=request.data.get('password')
            )
        # 이미 회원가입이 되어있는 유저일 경우
        if user is not None:
            serializer = LoginSerializer(instance=user)
            # jwt 토큰 접근
            token = TokenObtainPairSerializer().get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user" : serializer.data,
                    "message" : "login successfully",
                    "token" : {
                        "access" : access_token,
                        "refresh" : refresh_token,
                    },
                }, 
                status = status.HTTP_200_OK,
            )
            # jwt 토큰 쿠키에 넣어주기
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    # 로그아웃
    @swagger_auto_schema(tags=['로그인 및 인증'], responses={status.HTTP_200_OK: openapi.Response("Logout successfully")})
    def delete(self, request):
        res = Response(
            {"message" : "logout successfully"}, 
            status=status.HTTP_200_OK)
        res.delete_cookie("access")
        res.delete_cookie("refresh")
        return res
    
# 회원정보 수정
@swagger_auto_schema(tags=['회원정보 수정'], request_body=UserUpdateSerializer)
class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView): # RetrieveUpdateAPIView는 create를 제외한 Retrieve, Update 기능을 제공한다.
    permission_classes = [IsAuthenticated]
    renderer_classes = (JSONRenderer,)
    serializer_class = UserUpdateSerializer
    def get_object(self):
        return self.request.user # 현재 로그인한 유저의 정보를 실제 객체로 가져온다.
    def patch(self, request, *args, **kwargs):
        serializer = UserUpdateSerializer(instance=request.user, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True): # 유효성 검사를 한다
            serializer.save() # 저장한다.
            return Response(serializer.data, status=status.HTTP_200_OK) # 저장한 데이터를 반환한다.
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 유효성 검사에 실패하면 에러를 반환한다.

# 비밀번호 변경
class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = (JSONRenderer,)
    serializer_class = ChangePasswordSerializer
    
    @swagger_auto_schema(tags=['비밀번호 변경'], request_body=ChangePasswordSerializer)
    def post(self, request,*args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data,context={'request': request}) # request를 context로 넘겨주는 이유는 현재 로그인한 유저의 정보를 전달하기 위함이다.
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)