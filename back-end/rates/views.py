import os
from django.shortcuts import render
from rest_framework.views import APIView 
from django.conf import settings
from datetime import datetime
import requests
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import CurrencyRate
from rest_framework import status
from drf_yasg import openapi

API_KEY = os.environ['RATE_API_KEY']
# 현재 날짜를 YYYYMMDD 형식의 문자열로 변환
today = datetime.today().strftime('%Y%m%d')
# Create your views here.
class RatesListAPIView(APIView):
    url = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"
    
    def save_currency_to_db(self, currency_data):
        cur_nm = currency_data.get('cur_nm')
        cur_unit = currency_data.get('cur_unit')
        deal_bas_r = currency_data.get('deal_bas_r')
        # 기존 데이터를 업데이트하거나 새 데이터를 생성
        CurrencyRate.objects.update_or_create(
            cur_unit=cur_unit,
            defaults={'cur_nm': cur_nm, 'deal_bas_r': deal_bas_r}
        )

    @swagger_auto_schema(
        operation_summary="현재 환율 정보를 조회 및 DB에 저장합니다.",
        responses={200: "Success"},
        tags=['현재 환율']
    )
    def get(self, request):
        try:
            # API 요청을 보내기
            response = requests.get(self.url, params={
                'authkey': API_KEY,
                'searchdate': today,
                'data': 'AP01'
            })
            response.raise_for_status()  # HTTP 에러가 발생하면 예외를 발생시킴
            
            # API 응답 데이터를 JSON으로 파싱
            json_data = response.json()
            
            # 필요한 정보를 추출하여 반환
            currency_rates = {}
            for currency_data in json_data:
                cur_unit = currency_data.get('cur_unit')
                deal_bas_r = currency_data.get('deal_bas_r')
                currency_rates[cur_unit] = deal_bas_r
                # 데이터베이스에 저장
                self.save_currency_to_db(currency_data)
            
            return Response({'currency_rates': currency_rates}, status=status.HTTP_200_OK)
        
        except requests.exceptions.RequestException as e:
            # API 요청 중 에러 발생 시
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 환전 금액을 계산하는 API
class ExchangeMoneyAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="환율을 기반으로 두 통화 간의 금액 변환",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT, # 요청 바디의 타입
            required=['amount', 'from_currency', 'to_currency'], # 필수 요청 바디 파라미터
            properties={ # 요청 바디의 스키마
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='변환할 금액'), # 요청 바디의 amount 필드
                'from_currency': openapi.Schema(type=openapi.TYPE_STRING, description='변환할 통화'), # 요청 바디의 from_currency 필드
                'to_currency': openapi.Schema(type=openapi.TYPE_STRING, description='변환하고 싶은 통화') # 요청 바디의 to_currency 필드
            },
        ),
        responses={
            200: openapi.Response(
                description='Conversion result',
                examples={
                    'application/json': {
                        'result': 1234.56
                    }
                }
            ),
            404: openapi.Response(description='환율 정보를 찾을 수 없음'),
            500: openapi.Response(description='서버 내부 오류')
        },
        tags=['환율 변환']
    )
    def post(self, request):
        try:
            # 사용자가 입력한 환율 정보를 가져옴
            data = request.data
            amount = data.get('amount')
            from_currency = data.get('from_currency')
            to_currency = data.get('to_currency')
            
            # 데이터베이스에서 해당 환율 정보를 가져옴
            from_currency_rate = CurrencyRate.objects.get(cur_unit=from_currency)
            to_currency_rate = CurrencyRate.objects.get(cur_unit=to_currency)
            
            # 환율 계산 (기준이 되는 통화를 원화로 가정하고 계산)
            deal_bas_r_from = float(from_currency_rate.deal_bas_r.replace(',', ''))
            deal_bas_r_to = float(to_currency_rate.deal_bas_r.replace(',', ''))

            # 1 from_currency 단위를 원화로 변환한 후, 원하는 to_currency 단위로 변환
            result = (amount * deal_bas_r_from) / deal_bas_r_to
            
            return Response({'result': result}, status=status.HTTP_200_OK)
        
        except CurrencyRate.DoesNotExist:
            # 환율 정보가 없는 경우
            return Response({'error': '환율 정보가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # 기타 에러 발생 시
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)