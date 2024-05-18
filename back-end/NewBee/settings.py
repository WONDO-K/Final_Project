"""
Django settings for NewBee project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from datetime import timedelta
from pathlib import Path

import os
import environ
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

RATE_API_KEY = env('RATE_API_KEY')
PRODUCT_API_KEY = env('PRODUCT_API_KEY')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'accounts',
    'articles',
    'rates',
    'products',
    'drf_yasg',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS 설정 - whitelist 에 추가된 주소 접근 허용
CORS_ORIGIN_WHITELIST = ['http://127.0.0.1:8000' ,'http://localhost:5173']
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'NewBee.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'NewBee.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

## JWT 관련 세팅

# accounts 앱에서 내가 설정한 User를 사용하겠다고 설정한다.
AUTH_USER_MODEL = 'accounts.User'

# jwt 토큰은 simplejwt의 JWTAuthentication으로 인증한다.
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.permissions.IsAuthenticated', # 인증된 사용자만 접근
        # 'rest_framework.permissions.IsAdminUser', # 관리자만 접근
        # 'rest_framework.permissions.AllowAny', # 누구나 접근    
    ),
}

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'BearerAuth': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': "JWT Token"
        }
    },
    'SECURITY_REQUIREMENTS': [{
        'BearerAuth': []
    }]
}

# jwt settings
SIMPLE_JWT = {
# Access Token의 수명 (30분)
'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),

# Refresh Token의 수명 (7일)
'REFRESH_TOKEN_LIFETIME': timedelta(days=7),

# Refresh Token을 회전시킬지 여부 (False로 설정하면 Refresh Token이 회전되지 않음)
'ROTATE_REFRESH_TOKENS': False,

# Refresh Token 회전 후 이전 토큰을 블랙리스트에 추가할지 여부 (False로 설정하면 블랙리스트에 추가되지 않음)
'BLACKLIST_AFTER_ROTATION': False,

# 사용자의 마지막 로그인 시간을 업데이트할지 여부 (False로 설정하면 마지막 로그인 시간이 업데이트되지 않음)
'UPDATE_LAST_LOGIN': False,

# JWT 알고리즘 (HS256)
'ALGORITHM': 'HS256',

# 서명 키 (SECRET_KEY로 설정)
'SIGNING_KEY': SECRET_KEY,

# 검증 키 (사용되지 않음)
'VERIFYING_KEY': None,

# JWT의 대상 (사용되지 않음)
'AUDIENCE': None,

# JWT의 발급자 (사용되지 않음)
'ISSUER': None,

# JWK URL (사용되지 않음)
'JWK_URL': None,

# 시간 허용 범위 (0)
'LEEWAY': 0,

# 인증 헤더 타입 (Bearer)
'AUTH_HEADER_TYPES': ('Bearer',),

# 인증 헤더 이름 (HTTP_AUTHORIZATION)
'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',

# 사용자 ID 필드 (id)
'USER_ID_FIELD': 'id',

# 사용자 ID 클레임 (user_id)
'USER_ID_CLAIM': 'user_id',

# 사용자 인증 규칙 (rest_framework_simplejwt.authentication.default_user_authentication_rule)
'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

# 인증 토큰 클래스 (AccessToken)
'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),

# 토큰 타입 클레임 (token_type)
'TOKEN_TYPE_CLAIM': 'token_type',

# 토큰 사용자 클래스 (rest_framework_simplejwt.models.TokenUser)
'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

# JTI 클레임 (jti)
'JTI_CLAIM': 'jti',

# 슬라이딩 토큰 갱신 만료 클레임 (refresh_exp)
'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',

# 슬라이딩 토큰 수명 (5분)
'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),

# 슬라이딩 토큰 갱신 수명 (1일)
'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),

}
