import os
import requests
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.http import JsonResponse 
from drf_yasg.utils import swagger_auto_schema
from .serializers import *

from .models import Bank, Option

PRODUCT_API_KEY = os.environ['PRODUCT_API_KEY']

class BankListAPIView(APIView):
    url = f'http://finlife.fss.or.kr/finlifeapi/companySearch.json?auth={PRODUCT_API_KEY}&topFinGrpNo=020000&pageNo=1'

    def save_bank_to_db(self, bank_data, option_list):
        fin_co_no = bank_data.get('fin_co_no')
        kor_co_nm = bank_data.get('kor_co_nm')
        homp_url = bank_data.get('homp_url')
        cal_tel = bank_data.get('cal_tel')
        bank, created = Bank.objects.update_or_create(
            fin_co_no=fin_co_no,
            defaults={'kor_co_nm': kor_co_nm, 'homp_url': homp_url, 'cal_tel': cal_tel}
        )
        if created:
            self.save_option_to_db(bank, option_list)

    def save_option_to_db(self, bank, option_list):
        for option_data in option_list:
            area_cd = option_data.get('area_cd')
            area_nm = option_data.get('area_nm')
            exis_yn = option_data.get('exis_yn')
            Option.objects.create(
                bank=bank,
                area_cd=area_cd,
                area_nm=area_nm,
                exis_yn=exis_yn
            )

    @swagger_auto_schema(
        operation_summary="외부 API에서 은행 목록을 가져와 데이터베이스에 저장합니다.",
        responses={200: "성공"},
        tags=['은행']
    )
    def get(self, request):
        response = requests.get(self.url).json()
        base_list = response.get('result', {}).get('baseList', []) 
        option_list = response.get('result', {}).get('optionList', []) 

        # print(f'options: {option_list}')

        for bank_data in base_list:
            self.save_bank_to_db(bank_data, option_list)  # 옵션 리스트도 함께 전달

        return JsonResponse({"message": "은행 정보가 성공적으로 저장되었습니다."})

@swagger_auto_schema(
    operation_summary="은행의 상세 정보를 가져옵니다.",
    tags=['은행'])
class BankDetailAPIView(APIView):
    def get(self, request, bank_pk):
        bank = get_object_or_404(Bank, pk=bank_pk)
        bank_serializer = BankSerializer(bank)
        options = Option.objects.filter(bank=bank)
        options_serializer = OptionSerializer(options, many=True)
        data = {
            'bank': bank_serializer.data,
            'options': options_serializer.data
        }
        return JsonResponse(data)