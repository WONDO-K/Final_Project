import os
import requests
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.http import JsonResponse 
from drf_yasg.utils import swagger_auto_schema
from .serializers import *
from .models import Bank, BankOption, DepositProduct, DepositProductOption, SavingProduct, SavingProductOption, PensionProduct, PensionProductOption, RentLoanProduct, RentLoanProductOption


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
        tags=['금융']
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
    tags=['금융']
    )
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

@swagger_auto_schema(
    operation_summary="은행의 금융 상품 리스트를 가져옵니다.",
    tags=['조회']
    )   
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
    tags=['금융']
    )        
    def get(self, request):
        response = requests.get(self.url).json()
        product_list = response.get('result', {}).get('baseList', []) # baseList에 상품 정보가 들어있음
        option_list = response.get('result', {}).get('optionList', []) # optionList에 상품 옵션 정보가 들어있음

        for product_data in product_list:
            self.save_depoist_product_to_db(product_data, option_list) # 옵션 리스트도 함께 전달

        return JsonResponse({"message": "정기예금 상품 정보가 성공적으로 저장되었습니다."},status=201)
    
@swagger_auto_schema(
    operation_summary="정기예금의 상세 정보를 가져옵니다.",
    tags=['조회']
)
class DepositProductDetailAPIView(APIView):
    def get(self, request, product_pk):
        product = get_object_or_404(DepositProduct, pk=product_pk)
        product_serializer = DepositProductSerializer(product)
        return JsonResponse(product_serializer.data)
    
# 적금 --------------------------------------------------------

class SavingProductRegisterAPIView(APIView):
    url = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'

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
    tags=['금융']
    )
    def get(self, request):
        response = requests.get(self.url).json()
        product_list = response.get('result', {}).get('baseList', [])
        option_list = response.get('result', {}).get('optionList', [])

        for product_data in product_list:
            self.save_depoist_product_to_db(product_data, option_list)

        return JsonResponse({"message": "적금 상품 정보가 성공적으로 저장되었습니다."},status=201)

@swagger_auto_schema(
    operation_summary="적금 상품의 상세 정보를 가져옵니다.",
    tags=['조회']
)
class SavingProductDetailAPIView(APIView):
    def get(self, request, product_pk):
        product = get_object_or_404(SavingProduct, pk=product_pk)
        product_serializer = SavingProductSerializer(product)
        return JsonResponse(product_serializer.data)


# 연금 --------------------------------------------------------


class PensionProductRegisterAPIView(APIView):
    url = f'http://finlife.fss.or.kr/finlifeapi/annuitySavingProductsSearch.json?auth={API_KEY}&topFinGrpNo=060000&pageNo=1'

    def save_pension_product_to_db(self, product_data, option_list):
        fin_prdt_cd = product_data.get('fin_prdt_cd')
        fin_co_no = product_data.get('fin_co_no')
        kor_co_nm = product_data.get('kor_co_nm')
        fin_prdt_nm = product_data.get('fin_prdt_nm')
        join_way = product_data.get('join_way')
        pnsn_kind = product_data.get('pnsn_kind')
        pnsn_kind_nm = product_data.get('pnsn_kind_nm')
        sale_strt_day = product_data.get('sale_strt_day')
        mntn_cnt = product_data.get('mntn_cnt')
        prdt_type = product_data.get('prdt_type')
        prdt_type_nm = product_data.get('prdt_type_nm')
        dcls_rate = product_data.get('dcls_rate')
        guar_rate = product_data.get('guar_rate')
        btrm_prft_rate_1 = product_data.get('btrm_prft_rate_1')
        btrm_prft_rate_2 = product_data.get('btrm_prft_rate_2')
        btrm_prft_rate_3 = product_data.get('btrm_prft_rate_3')
        etc = product_data.get('etc')
        sale_co = product_data.get('sale_co')
        dcls_strt_day = product_data.get('dcls_strt_day')
        dcls_end_day = product_data.get('dcls_end_day')
        fin_co_subm_day = product_data.get('fin_co_subm_day')

        # PensionProduct 객체 생성 또는 업데이트
        pension_product, created = PensionProduct.objects.update_or_create(
            fin_prdt_cd=fin_prdt_cd,
            defaults={
                'fin_co_no': fin_co_no,
                'kor_co_nm': kor_co_nm,
                'fin_prdt_nm': fin_prdt_nm,
                'join_way': join_way,
                'pnsn_kind': pnsn_kind,
                'pnsn_kind_nm': pnsn_kind_nm,
                'sale_strt_day': sale_strt_day,
                'mntn_cnt': mntn_cnt,
                'prdt_type': prdt_type,
                'prdt_type_nm': prdt_type_nm,
                'dcls_rate': dcls_rate,
                'guar_rate': guar_rate,
                'btrm_prft_rate_1': btrm_prft_rate_1,
                'btrm_prft_rate_2': btrm_prft_rate_2,
                'btrm_prft_rate_3': btrm_prft_rate_3,
                'etc': etc,
                'sale_co': sale_co,
                'dcls_strt_day': dcls_strt_day,
                'dcls_end_day': dcls_end_day,
                'fin_co_subm_day': fin_co_subm_day
            }
        )

        # PensionProductOption 객체 생성
        for option_data in option_list:
            if option_data.get('fin_prdt_cd') == fin_prdt_cd:
                dcls_month = option_data.get('dcls_month')
                fin_co_no = option_data.get('fin_co_no')
                fin_prdt_cd = option_data.get('fin_prdt_cd')
                pnsn_recp_trm = option_data.get('pnsn_recp_trm')
                pnsn_recp_trm_nm = option_data.get('pnsn_recp_trm_nm')
                pnsn_entr_age = option_data.get('pnsn_entr_age')
                pnsn_entr_age_nm = option_data.get('pnsn_entr_age_nm')
                mon_paym_atm = option_data.get('mon_paym_atm')
                mon_paym_atm_nm = option_data.get('mon_paym_atm_nm')
                paym_prd = option_data.get('paym_prd')
                paym_prd_nm = option_data.get('paym_prd_nm')
                pnsn_strt_age = option_data.get('pnsn_strt_age')
                pnsn_strt_age_nm = option_data.get('pnsn_strt_age_nm')
                pnsn_recp_amt = option_data.get('pnsn_recp_amt')

                PensionProductOption.objects.create(
                    pension_product=pension_product,
                    dcls_month=dcls_month,
                    fin_co_no=fin_co_no,
                    fin_prdt_cd=fin_prdt_cd,
                    pnsn_recp_trm=pnsn_recp_trm,
                    pnsn_recp_trm_nm=pnsn_recp_trm_nm,
                    pnsn_entr_age=pnsn_entr_age,
                    pnsn_entr_age_nm=pnsn_entr_age_nm,
                    mon_paym_atm=mon_paym_atm,
                    mon_paym_atm_nm=mon_paym_atm_nm,
                    paym_prd=paym_prd,
                    paym_prd_nm=paym_prd_nm,
                    pnsn_strt_age=pnsn_strt_age,
                    pnsn_strt_age_nm=pnsn_strt_age_nm,
                    pnsn_recp_amt=pnsn_recp_amt
                )

    @swagger_auto_schema(
        operation_summary="외부 API에서 연금 상품 정보를 가져와 데이터베이스에 저장합니다.",
        tags=['금융']
    )
    def get(self, request):
        response = requests.get(self.url).json()
        product_list = response.get('result', {}).get('baseList', [])
        option_list = response.get('result', {}).get('optionList', [])

        for product_data in product_list:
            self.save_pension_product_to_db(product_data, option_list)

        return JsonResponse({"message": "연금 상품 정보가 성공적으로 저장되었습니다."}, status=201)


@swagger_auto_schema(
    operation_summary="연금 상품의 상세 정보를 가져옵니다.",
    tags=['조회']
)
class PensionProductDetailAPIView(APIView):
    def get(self, request, product_pk):
        product = get_object_or_404(PensionProduct, pk=product_pk)
        product_serializer = PensionProductSerializer(product)
        return JsonResponse(product_serializer.data)

# 전세대출 --------------------------------------------------------
class RentLoanProductRegisterAPIView(APIView):
    url = f'http://finlife.fss.or.kr/finlifeapi/rentHouseLoanProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'

    def save_rent_loan_to_db(self, product_data, option_list):
        fin_prdt_cd = product_data.get('fin_prdt_cd')
        fin_co_no = product_data.get('fin_co_no')
        fin_co_instance = Bank.objects.get(fin_co_no=fin_co_no)
        kor_co_nm = product_data.get('kor_co_nm')
        fin_prdt_nm = product_data.get('fin_prdt_nm')
        join_way = product_data.get('join_way')
        loan_inci_expn = product_data.get('loan_inci_expn')
        erly_rpay_fee = product_data.get('erly_rpay_fee')
        dly_rate = product_data.get('dly_rate')
        loan_lmt = product_data.get('loan_lmt')
        dcls_strt_day = product_data.get('dcls_strt_day')
        dcls_end_day = product_data.get('dcls_end_day')
        dcls_month = product_data.get('dcls_month')
        fin_co_subm_day = product_data.get('fin_co_subm_day')

        # Bank 객체를 가져와서 넣어줌
        fin_co_instance = Bank.objects.get(fin_co_no=fin_co_no)

        # RentLoan 객체 생성 또는 업데이트
        rent_loan_product, created = RentLoanProduct.objects.update_or_create(
            fin_prdt_cd=fin_prdt_cd, 
            defaults={
                'fin_co_no': fin_co_instance,  # Bank 객체를 넣어줌
                'kor_co_nm': kor_co_nm,
                'fin_prdt_nm': fin_prdt_nm,
                'join_way': join_way,
                'loan_inci_expn': loan_inci_expn,
                'erly_rpay_fee': erly_rpay_fee,
                'dly_rate': dly_rate,
                'loan_lmt': loan_lmt,
                'dcls_strt_day': dcls_strt_day,
                'dcls_end_day': dcls_end_day,
                'dcls_month': dcls_month,
                'fin_co_subm_day': fin_co_subm_day
            }
        )

        # RentLoanOption 객체 생성
        for option_data in option_list:
            RentLoanProductOption.objects.create(
                rent_loan_product=rent_loan_product,
                dcls_month=option_data.get('dcls_month'),
                fin_co_no=option_data.get('fin_co_no'),
                fin_prdt_cd=option_data.get('fin_prdt_cd'),
                rpay_type=option_data.get('rpay_type'),
                rpay_type_nm=option_data.get('rpay_type_nm'),
                lend_rate_type=option_data.get('lend_rate_type'),
                lend_rate_type_nm=option_data.get('lend_rate_type_nm'),
                lend_rate_min=option_data.get('lend_rate_min'),
                lend_rate_max=option_data.get('lend_rate_max'),
                lend_rate_avg=option_data.get('lend_rate_avg')
            )
    @swagger_auto_schema(
        operation_summary="외부 API에서 전월세보증금대출 상품 정보를 가져와 데이터베이스에 저장합니다.",
        tags=['금융']
    )
    def get(self, request):
        response = requests.get(self.url).json()
        product_list = response.get('result', {}).get('baseList', [])
        option_list = response.get('result', {}).get('optionList', [])

        for product_data in product_list:
            product_options = [opt for opt in option_list if opt.get('fin_prdt_cd') == product_data.get('fin_prdt_cd')]
            self.save_rent_loan_to_db(product_data, product_options)

        return JsonResponse({"message": "전월세보증금대출 상품 정보가 성공적으로 저장되었습니다."}, status=201)
    
class RentLoanDetailAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="전월세보증금대출 상품의 상세 정보를 가져옵니다.",
        tags=['조회']
    )
    def get(self, request, product_pk):
        rent_loan = get_object_or_404(RentLoanProduct, pk=product_pk)
        rent_loan_serializer = RentLoanSerializer(rent_loan)
        return JsonResponse(rent_loan_serializer.data)

from .models.UserProducts import UserDepositProduct, UserSavingProduct, UserPensionProduct, UserRentLoanProduct    
from drf_yasg import openapi
from django.utils import timezone

# 현재 로그인한 유저의 가입 상품 조회 --------------------------------------------------------
class UserProductListView(APIView):
    @swagger_auto_schema(
        operation_summary="현재 로그인한 사용자의 가입 상품을 조회합니다.",
        responses={200: "가입 상품 목록", 401: "인증 실패"},
        tags=['가입한 상품 조회']
    )
    def get(self, request, *args, **kwargs):
        user = self.request.user
        
        deposit_products = UserDepositProduct.objects.filter(user=user)
        saving_products = UserSavingProduct.objects.filter(user=user)
        pension_products = UserPensionProduct.objects.filter(user=user)
        rent_loan_products = UserRentLoanProduct.objects.filter(user=user)

        deposit_serializer = UserDepositProductSerializer(deposit_products, many=True)
        saving_serializer = UserSavingProductSerializer(saving_products, many=True)
        pension_serializer = UserPensionProductSerializer(pension_products, many=True)
        rent_loan_serializer = UserRentLoanProductSerializer(rent_loan_products, many=True)

        products = deposit_serializer.data + saving_serializer.data + pension_serializer.data + rent_loan_serializer.data
        return JsonResponse({"products": products}, status=200)
    
# 상품 가입 --------------------------------------------------------
class JoinProductAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="사용자가 상품에 가입합니다.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['정기예금', '적금', '연금', '전세대출'],
                    description="상품 유형을 선택하세요."
                ),
                'product_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="상품 ID를 입력하세요."
                ),
                'option_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="옵션 ID를 입력하세요."
                )
            },
            required=['product_type', 'product_id', 'option_id']
        ),
        responses={201: "가입 성공", 400: "잘못된 요청"},
        examples={
            "application/json": {
                "product_type": "정기예금",
                "product_id": 1,
                "option_id": 1
            } 
        }
    )
    def post(self, request):
        serializer = JoinProductSerializer(data=request.data) 
        if serializer.is_valid():
            product_type = serializer.validated_data['product_type']
            product_id = serializer.validated_data['product_id']
            option_id = serializer.validated_data['option_id']
            try:
                product, option = get_product_and_option_models(product_type, product_id, option_id)
            except ValueError as e:
                return JsonResponse({"message": str(e)}, status=400)

            # 각 상품 유형에 따라 올바른 시리얼라이저를 사용하여 유효성 검사하고 처리
            if product_type == '정기예금':
                user_product_serializer = UserDepositProductSerializer(data={
                    'user': request.user.pk,
                    'product_type': product_type,
                    'selected_option': option.pk,
                    'deposit_product': product.pk,
                    'join_date': timezone.now().date()
                })
            elif product_type == '적금':
                user_product_serializer = UserSavingProductSerializer(data={
                    'user': request.user.pk,
                    'product_type': product_type,
                    'selected_option': option.pk,
                    'saving_product': product.pk,
                    'join_date': timezone.now().date()
                })
            elif product_type == '연금':
                user_product_serializer = UserPensionProductSerializer(data={
                    'user': request.user.pk,
                    'product_type': product_type,
                    'selected_option': option.pk,
                    'pension_product': product.pk,
                    'join_date': timezone.now().date()
                })
            elif product_type == '전세대출':
                user_product_serializer = UserRentLoanProductSerializer(data={
                    'user': request.user,
                    'product_type': product_type,
                    'selected_option': option.pk,
                    'rent_loan_product': product.pk,
                    'join_date': timezone.now().date()
                })
            else:
                return JsonResponse({"message": "잘못된 상품 타입입니다."}, status=400)
            
            if user_product_serializer.is_valid():
                user_product_serializer.save()
                return JsonResponse({"message": "가입이 성공적으로 완료되었습니다."}, status=201)
            else:
                return JsonResponse({"message": "잘못된 사용자 상품 정보입니다.", "errors": user_product_serializer.errors}, status=400)
        else:
            return JsonResponse(serializer.errors, status=400)


        
def get_product_and_option_models(product_type, product_id, option_id):
    if product_type == '정기예금':
        product = DepositProduct.objects.get(pk=product_id)
        option = DepositProductOption.objects.get(pk=option_id)
        return product, option
    elif product_type == '적금':
        product = SavingProduct.objects.get(pk=product_id)
        option = SavingProductOption.objects.get(pk=option_id)
        return product, option
    elif product_type == '연금':
        product = PensionProduct.objects.get(pk=product_id)
        option = PensionProductOption.objects.get(id=option_id)
        return product, option
    elif product_type == '전세대출':
        product = RentLoanProduct.objects.get(pk=product_id)
        option = RentLoanProductOption.objects.get(id=option_id)
        return product, option
    else:
        raise ValueError("잘못된 정보입니다.")