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
        CurrencyRate.objects.create(cur_nm=cur_nm, cur_unit=cur_unit, deal_bas_r=deal_bas_r)

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
