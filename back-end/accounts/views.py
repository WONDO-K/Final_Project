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
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError


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

# 유저 ID 중복 확인
class UsernameCheckAPIView(APIView):
    @swagger_auto_schema(tags=['회원가입'], manual_parameters=[
        # openapi.Parameter를 사용하는 의미는 swagger에서 해당 파라미터를 보여주기 위함이다. -> 즉, Swagger에서만 사용되는 값이다.
        # 프론트에서는 값을 입력하고 중복확인 버튼을 누르면 검증이 이루어지기 때문에 프론트에서는 필요없는 값이다.
        # type=openapi.TYPE_STRING는 해당 파라미터의 타입을 지정해주는 것이다.
        openapi.Parameter('username', openapi.IN_QUERY, description="아이디 중복을 체크합니다.", type=openapi.TYPE_STRING)
    ])
    def get(self, request):
        username = request.query_params.get('username', None) # None은 username이 없을 경우 None을 반환한다.
        if username:
            # 아이디 형식을 검증하는 정규식
            username_regex = r'^[a-z0-9]{3,30}$'
            username_validator = RegexValidator(
                regex=username_regex,
                message=_("아이디는 3~30자의 영문 소문자, 숫자로 이루어져야 합니다.") # _는 Django의 내장 함수인 gettext()의 축약형으로 유효성 검사 오류 메시지를 번역하기 위해 사용한다.
            )

            try:
                username_validator(username)
            except ValidationError  as e: # ValidationError가 발생하면 ValidationError 메시지를 반환한다.
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST) 
            
            if User.objects.filter(username=username).exists(): # username이 이미 존재하는지 확인 후 exists()로 존재하면 True, 존재하지 않으면 False를 반환한다.
                return Response({"message": "해당 아이디가 이미 존재합니다."}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"message": "사용 가능한 아이디입니다."}, status=status.HTTP_200_OK)
        
        return Response({"message": "username을 제공해야 합니다."}, status=status.HTTP_400_BAD_REQUEST)

    
# 이메일 중복 확인
class EmailCheckAPIView(APIView):
    @swagger_auto_schema(tags=['회원가입'], manual_parameters=[
        openapi.Parameter('email', openapi.IN_QUERY, description="이메일 중복을 체크합니다.", type=openapi.TYPE_STRING)
    ])
    def get(self, request):
        email = request.query_params.get('email', None)
        if email:
            # 이메일 형식을 검증하는 정규식
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            email_validator = RegexValidator(
                regex=email_regex,
                message=_("유효한 이메일 주소 형식이 아닙니다.")
            )

            try:
                email_validator(email)
            except ValidationError  as e: # ValidationError가 발생하면 ValidationError 메시지를 반환한다.
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(email=email).exists():
                return Response({"message": "해당 이메일이 이미 존재합니다."}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"message": "사용 가능한 이메일입니다."}, status=status.HTTP_200_OK)
        
        return Response({"message": "email을 제공해야 합니다."}, status=status.HTTP_400_BAD_REQUEST)


# 로그인 및 인증
class AuthAPIView(APIView):
    # 유저 정보 가져오기
    @swagger_auto_schema(tags=['로그인 및 인증'])
    def get(self, request):
        try:
            # Authorization 헤더에서 액세스 토큰 추출
            authorization_header = request.headers.get('Authorization')
            if not authorization_header or not authorization_header.startswith('Bearer '):
                return Response({"detail": "액세스 토큰을 찾을 수 없습니다."}, status=status.HTTP_401_UNAUTHORIZED)

            access = authorization_header.split('Bearer ')[1]

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
                user_serializer = UserSerializer(instance=user)

                # 새로 발급된 Access 토큰과 Refresh 토큰을 쿠키에 설정
                res = Response(user_serializer.data, status=status.HTTP_200_OK)
                res.set_cookie(
                    key='access',
                    value=access,
                    httponly=True,
                    secure=False,  # HTTPS를 사용하는 경우
                    samesite='None'  # Cross-site 쿠키를 사용하기 위해 설정
                )
                res.set_cookie(
                    key='refresh',
                    value=refresh,
                    httponly=True,
                    secure=False,  # HTTPS를 사용하는 경우
                    samesite='None'  # Cross-site 쿠키를 사용하기 위해 설정
                )
                return res
            return Response({"detail": "잘못된 리프래쉬 토큰입니다."}, status=status.HTTP_401_UNAUTHORIZED)
        except (jwt.exceptions.InvalidTokenError):
            return Response({"detail": "잘못된 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST)
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
            res.set_cookie("access", access_token, httponly=True) # httponly=True는 자바스크립트에서 쿠키에 접근하지 못하도록 하는 옵션이다.
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