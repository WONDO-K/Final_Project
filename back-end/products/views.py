import os
import requests
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.http import JsonResponse 
from drf_yasg.utils import swagger_auto_schema
from .serializers import *

from .models import *

API_KEY = os.environ['PRODUCT_API_KEY']

class BankRegisterAPIView(APIView):
    url = f'http://finlife.fss.or.kr/finlifeapi/companySearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'

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
            BankOption.objects.create(
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
        options = BankOption.objects.filter(bank=bank)
        options_serializer = BankOptionSerializer(options, many=True)
        data = {
            'bank': bank_serializer.data,
            'options': options_serializer.data
        }
        return JsonResponse(data)
    

# 정기예금 --------------------------------------------------------
class DepositProductRegisterAPIView(APIView):
    url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'

    def save_depoist_product_to_db(self, product_data, option_list):
        fin_prdt_cd = product_data.get('fin_prdt_cd')
        fin_co_no = product_data.get('fin_co_no')
        fin_co_instance = Bank.objects.get(fin_co_no=fin_co_no) # Bank 객체를 가져와서 넣어줘야 함
        fin_prdt_nm = product_data.get('fin_prdt_nm')
        join_way = product_data.get('join_way')
        mtrt_int = product_data.get('mtrt_int')
        spcl_cnd = product_data.get('spcl_cnd')
        join_deny = product_data.get('join_deny')
        join_member = product_data.get('join_member')
        etc_note = product_data.get('etc_note')
        max_limit = product_data.get('max_limit')
        dcls_strt_day = product_data.get('dcls_strt_day')
        dcls_end_day = product_data.get('dcls_end_day')
        fin_co_subm_day = product_data.get('fin_co_subm_day')

        # Product 객체 생성 또는 업데이트
        product, created = DepositProduct.objects.update_or_create(
            fin_prdt_cd=fin_prdt_cd,
            defaults={
                'fin_prdt_nm': fin_prdt_nm,
                'fin_co_no' :  fin_co_instance, # Bank 객체를 넣어줘야 함
                'join_way': join_way,
                'mtrt_int': mtrt_int,
                'spcl_cnd': spcl_cnd,
                'join_deny': join_deny,
                'join_member': join_member,
                'etc_note': etc_note,
                'max_limit': max_limit,
                'dcls_strt_day': dcls_strt_day,
                'dcls_end_day': dcls_end_day,
                'fin_co_subm_day': fin_co_subm_day
            }
        )

        # ProductOption 객체 생성
        for option_data in option_list:
            intr_rate_type = option_data.get('intr_rate_type')
            intr_rate_type_nm = option_data.get('intr_rate_type_nm')
            save_trm = option_data.get('save_trm')
            intr_rate = option_data.get('intr_rate')
            intr_rate2 = option_data.get('intr_rate2')

            DepositProductOption.objects.create(
                deposit_product=product,
                intr_rate_type=intr_rate_type,
                intr_rate_type_nm=intr_rate_type_nm,
                save_trm=save_trm,
                intr_rate=intr_rate,
                intr_rate2=intr_rate2
            )


    @swagger_auto_schema(
    operation_summary="외부 API에서 정기예금 상품 정보를 가져와 데이터베이스에 저장합니다.",
    tags=['정기예금'])        
    def get(self, request):
        response = requests.get(self.url).json()
        product_list = response.get('result', {}).get('baseList', [])
        option_list = response.get('result', {}).get('options', [])

        for product_data in product_list:
            self.save_depoist_product_to_db(product_data, option_list)

        return JsonResponse({"message": "상품 정보가 성공적으로 저장되었습니다."})
    
@swagger_auto_schema(
    operation_summary="정기예금의 상세 정보를 가져옵니다.",
    tags=['정기예금']
)
class DepositProductDetailAPIView(APIView):
    def get(self, request, product_pk):
        product = get_object_or_404(DepositProduct, pk=product_pk)
        product_serializer = DepositProductSerializer(product)
        return JsonResponse(product_serializer.data)