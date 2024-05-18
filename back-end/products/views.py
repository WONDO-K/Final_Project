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

        return JsonResponse({"message": "은행 정보가 성공적으로 저장되었습니다."},status=201) # 201 코드는 요청이 성공적으로 처리되었으며 그 결과로 새 리소스가 생성되었음을 나타냄

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
    
class BanksProductsAPIView(APIView):
    def get(self, request, bank_pk):
        bank = get_object_or_404(Bank, pk=bank_pk) # Bank 객체를 가져옴
        products = DepositProduct.objects.filter(fin_co_no=bank) # 해당 은행의 상품들을 가져옴
        product_serializer = DepositProductSerializer(products, many=True)
        return JsonResponse(product_serializer.data, safe=False) # safe=False로 설정하는 이유는 QuerySet이 직렬화되지 않기 때문
        # QuerySet이 직렬화되지 않는 이유는 QuerySet은 리스트와 비슷한 객체이지만 직렬화할 수 없는 객체이기 때문입니다.
    

# 정기예금 --------------------------------------------------------
class DepositProductRegisterAPIView(APIView):
    url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'

    def save_depoist_product_to_db(self, product_data, option_list):
        fin_prdt_cd = product_data.get('fin_prdt_cd') # 상품 코드
        fin_co_no = product_data.get('fin_co_no') # 금융회사 코드
        fin_co_instance = Bank.objects.get(fin_co_no=fin_co_no) # Bank 객체를 가져와서 넣어줘야 함
        fin_prdt_nm = product_data.get('fin_prdt_nm') # 상품명
        join_way = product_data.get('join_way') # 가입 방법
        mtrt_int = product_data.get('mtrt_int') # 만기 후 이자율     
        spcl_cnd = product_data.get('spcl_cnd') # 우대조건
        join_deny = product_data.get('join_deny') # 가입제한
        join_member = product_data.get('join_member') # 가입대상
        etc_note = product_data.get('etc_note') # 기타 유의사항
        max_limit = product_data.get('max_limit') # 최고한도
        dcls_strt_day = product_data.get('dcls_strt_day') # 공시 시작일
        dcls_end_day = product_data.get('dcls_end_day') # 공시 종료일
        fin_co_subm_day = product_data.get('fin_co_subm_day') # 금융회사 제출일

        # Product 객체 생성 또는 업데이트
        product, created = DepositProduct.objects.update_or_create( 
            fin_prdt_cd=fin_prdt_cd, # 상품 코드로 조회
            defaults={ # 업데이트할 필드들
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
        for option_data in option_list: # 옵션 리스트에서 해당 상품 코드를 가진 옵션만 가져옴
            intr_rate_type = option_data.get('intr_rate_type') # 이자율 종류
            intr_rate_type_nm = option_data.get('intr_rate_type_nm') # 이자율 종류명
            save_trm = option_data.get('save_trm') # 저축 기간
            intr_rate = option_data.get('intr_rate') # 이자율
            intr_rate2 = option_data.get('intr_rate2') # 이자율2

            DepositProductOption.objects.create( # DepositProductOption 객체 생성
                deposit_product=product, # Product 객체를 넣어줘야 함
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
        product_list = response.get('result', {}).get('baseList', []) # baseList에 상품 정보가 들어있음
        option_list = response.get('result', {}).get('optionList', []) # optionList에 상품 옵션 정보가 들어있음

        for product_data in product_list:
            self.save_depoist_product_to_db(product_data, option_list) # 옵션 리스트도 함께 전달

        return JsonResponse({"message": "정기예금 상품 정보가 성공적으로 저장되었습니다."},status=201)
    
@swagger_auto_schema(
    operation_summary="정기예금의 상세 정보를 가져옵니다.",
    tags=['정기예금']
)
class DepositProductDetailAPIView(APIView):
    def get(self, request, product_pk):
        product = get_object_or_404(DepositProduct, pk=product_pk)
        product_serializer = DepositProductSerializer(product)
        return JsonResponse(product_serializer.data)
    
# 적금 --------------------------------------------------------

class SavingProductRegisterAPIView(APIView):
    url = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'

    @swagger_auto_schema(
    operation_summary="외부 API에서 정기예금 상품 정보를 가져와 데이터베이스에 저장합니다.",
    tags=['정기예금'])   
    def save_depoist_product_to_db(self, product_data, option_list):
        fin_prdt_cd = product_data.get('fin_prdt_cd') # 상품 코드
        fin_co_no = product_data.get('fin_co_no') # 금융회사 코드
        kor_co_nm = product_data.get('kor_co_nm') # 금융회사명
        fin_co_instance = Bank.objects.get(fin_co_no=fin_co_no) # Bank 객체를 가져와서 넣어줘야 함
        fin_prdt_nm = product_data.get('fin_prdt_nm') # 상품명
        join_way = product_data.get('join_way') # 가입 방법
        mtrt_int = product_data.get('mtrt_int') # 만기 후 이자율     
        spcl_cnd = product_data.get('spcl_cnd') # 우대조건
        join_deny = product_data.get('join_deny') # 가입제한
        join_member = product_data.get('join_member') # 가입대상
        etc_note = product_data.get('etc_note') # 기타 유의사항
        max_limit = product_data.get('max_limit') # 최고한도
        dcls_strt_day = product_data.get('dcls_strt_day') # 공시 시작일
        dcls_end_day = product_data.get('dcls_end_day') # 공시 종료일
        dcls_month = product_data.get('dcls_month') # 공시 제출월
        fin_co_subm_day = product_data.get('fin_co_subm_day') # 금융회사 제출일

        # Product 객체 생성 또는 업데이트
        product, created = SavingProduct.objects.update_or_create( 
            fin_prdt_cd=fin_prdt_cd, # 상품 코드로 조회
            defaults={ # 업데이트할 필드들
                'fin_prdt_nm': fin_prdt_nm,
                'fin_co_no' :  fin_co_instance, # Bank 객체를 넣어줘야 함
                'kor_co_nm': kor_co_nm, # 금융회사명 추가
                'join_way': join_way,
                'mtrt_int': mtrt_int,
                'spcl_cnd': spcl_cnd,
                'join_deny': join_deny,
                'join_member': join_member,
                'etc_note': etc_note,
                'max_limit': max_limit,
                'dcls_strt_day': dcls_strt_day,
                'dcls_end_day': dcls_end_day,
                'dcls_month': dcls_month,
                'fin_co_subm_day': fin_co_subm_day
            }
        )

        # ProductOption 객체 생성
        for option_data in option_list:
            intr_rate_type = option_data.get('intr_rate_type')
            intr_rate_type_nm = option_data.get('intr_rate_type_nm')
            intr_rate = option_data.get('intr_rate')
            intr_rate2 = option_data.get('intr_rate2')
            rsrv_type = option_data.get('rsrv_type')
            rsrv_type_nm = option_data.get('rsrv_type_nm')
            save_trm = option_data.get('save_trm')
        
            SavingProductOption.objects.create(
                saving_product=product,
                intr_rate_type=intr_rate_type,
                intr_rate_type_nm=intr_rate_type_nm,
                intr_rate=intr_rate,
                intr_rate2=intr_rate2,
                rsrv_type=rsrv_type,
                rsrv_type_nm=rsrv_type_nm,
                save_trm=save_trm
            )
    @swagger_auto_schema(
    operation_summary="외부 API에서 적금 상품 정보를 가져와 데이터베이스에 저장합니다.",
    tags=['적금'])

    def get(self, request):
        response = requests.get(self.url).json()
        product_list = response.get('result', {}).get('baseList', [])
        option_list = response.get('result', {}).get('optionList', [])

        for product_data in product_list:
            self.save_depoist_product_to_db(product_data, option_list)

        return JsonResponse({"message": "적금 상품 정보가 성공적으로 저장되었습니다."},status=201)
    