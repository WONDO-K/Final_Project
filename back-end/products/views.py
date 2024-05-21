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

    @swagger_auto_schema(
        operation_summary="외부 API에서 은행 목록을 가져와 데이터베이스에 저장합니다.",
        responses={200: "성공"},
        tags=['은행']
    )
    def get(self, request):
        response = requests.get(self.url).json()

        base_list = response.get('result', {}).get('baseList', []) 
        option_list = response.get('result', {}).get('optionList', []) 

        for bank_data in base_list:
            serializer = BankSerializer(data=bank_data)
            if serializer.is_valid():
                bank = serializer.save()
                # 해당 은행과 관련된 옵션 데이터 필터링
                bank_option_data = [option_data for option_data in option_list if option_data.get('fin_co_no') == bank.fin_co_no]
                
                for option_data in bank_option_data:
                    option_serializer = BankOptionSerializer(data=option_data)
                    if option_serializer.is_valid():
                        option_serializer.save(bank=bank)

        return JsonResponse({"message": "은행 정보가 성공적으로 저장되었습니다."}, status=201)


class BankDetailAPIView(APIView):
    @swagger_auto_schema(
    operation_summary="은행의 상세 정보를 가져옵니다.",
    tags=['은행']
    )
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
    @swagger_auto_schema(
    operation_summary="은행의 금융 상품 리스트를 가져옵니다.",
    tags=['은행']
    )   
    def get(self, request, bank_pk):
        bank = get_object_or_404(Bank, pk=bank_pk) # Bank 객체를 가져옴
        products = DepositProduct.objects.filter(fin_co_no=bank) # 해당 은행의 상품들을 가져옴
        product_serializer = DepositProductSerializer(products, many=True)
        return JsonResponse(product_serializer.data, safe=False) # safe=False로 설정하는 이유는 QuerySet이 직렬화되지 않기 때문
        # QuerySet이 직렬화되지 않는 이유는 QuerySet은 리스트와 비슷한 객체이지만 직렬화할 수 없는 객체이기 때문입니다.
    

# 정기예금 --------------------------------------------------------
class DepositProductRegisterAPIView(APIView):
    url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'

    @swagger_auto_schema(
        operation_summary="외부 API에서 정기예금 상품 정보를 가져와 데이터베이스에 저장합니다.",
        tags=['정기예금']
    )
    def get(self, request):
        response = requests.get(self.url).json()
        
        base_list = response.get('result', {}).get('baseList', [])
        option_list = response.get('result', {}).get('optionList', [])

        # 먼저 모든 제품을 저장합니다.
        for product_data in base_list:
            fin_prdt_cd = product_data.get('fin_prdt_cd')
            # 중복 확인
            if not DepositProduct.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
                fin_co_no = product_data.get('fin_co_no')
                fin_co_instance = Bank.objects.get(fin_co_no=fin_co_no)
                serializer = DepositProductSerializer(data=product_data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(fin_co_no=fin_co_instance)  # 변경된 부분
            
        # 각 제품에 해당하는 옵션을 저장합니다.
        for option_data in option_list:
            fin_prdt_cd = option_data.get('fin_prdt_cd')
            product = DepositProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
            serializer = DepositOptionsSerializer(data=option_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(deposit_product=product)

        return JsonResponse({"message": "정기예금 상품 정보가 성공적으로 저장되었습니다."}, status=201)


class DepositProductDetailAPIView(APIView):
    @swagger_auto_schema(
    operation_summary="정기예금의 상세 정보를 가져옵니다.",
    tags=['정기예금']
    )
    def get(self, request, product_pk):
        product = get_object_or_404(DepositProduct, pk=product_pk)
        product_serializer = DepositProductSerializer(product)
        return JsonResponse(product_serializer.data)
    
# 적금 --------------------------------------------------------
class SavingProductRegisterAPIView(APIView):
    url = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'

    @swagger_auto_schema(
        operation_summary="외부 API에서 적금 상품 정보를 가져와 데이터베이스에 저장합니다.",
        tags=['적금']
    )
    def get(self, request):
        response = requests.get(self.url).json()
        product_list = response.get('result', {}).get('baseList', [])
        option_list = response.get('result', {}).get('optionList', [])

        # 적금 상품 정보를 가져와 데이터베이스에 저장합니다.
        for product_data in product_list:
            fin_prdt_cd = product_data.get('fin_prdt_cd')
            # 중복 확인
            if not SavingProduct.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
                fin_co_no = product_data.get('fin_co_no')
                fin_co_instance = Bank.objects.get(fin_co_no=fin_co_no)
                serializer = SavingProductSerializer(data=product_data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(fin_co_no=fin_co_instance)

        # 적금 상품 옵션 정보를 가져와 데이터베이스에 저장합니다.
        for option_data in option_list:
            fin_prdt_cd = option_data.get('fin_prdt_cd')
            product = SavingProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
            serializer = SavingProductOptionSerializer(data=option_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(saving_product=product)

        return JsonResponse({"message": "적금 상품 정보가 성공적으로 저장되었습니다."}, status=201)

class SavingProductDetailAPIView(APIView):
    @swagger_auto_schema(
    operation_summary="적금 상품의 상세 정보를 가져옵니다.",
    tags=['적금'])
    def get(self, request, product_pk):
        product = get_object_or_404(SavingProduct, pk=product_pk)
        product_serializer = SavingProductSerializer(product)
        return JsonResponse(product_serializer.data)


# 연금 --------------------------------------------------------

class PensionProductRegisterAPIView(APIView):
    url = f'http://finlife.fss.or.kr/finlifeapi/annuitySavingProductsSearch.json?auth={API_KEY}&topFinGrpNo=060000&pageNo=1'
    
    @swagger_auto_schema(
        operation_summary="외부 API에서 연금 저축 상품 정보를 가져와 데이터베이스에 저장합니다.",
        tags=['연금']
    )
    def get(self, request):
        response = requests.get(self.url).json()
        product_list = response.get('result', {}).get('baseList', [])
        option_list = response.get('result', {}).get('optionList', [])

        # 연금 상품 정보를 가져와 데이터베이스에 저장합니다.
        for product_data in product_list:
            fin_prdt_cd = product_data.get('fin_prdt_cd')
            # 중복 확인
            if not PensionProduct.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
                serializer = PensionProductSerializer(data=product_data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()

        # 연금 상품 옵션 정보를 가져와 데이터베이스에 저장합니다.
        for option_data in option_list:
            fin_prdt_cd = option_data.get('fin_prdt_cd')
            product = PensionProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
            serializer = PensionProductOptionSerializer(data=option_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(pension_product=product)

        return JsonResponse({"message": "연금 상품 정보가 성공적으로 저장되었습니다."}, status=201)


class PensionProductDetailAPIView(APIView):
    @swagger_auto_schema(
    operation_summary="연금 상품의 상세 정보를 가져옵니다.",
    tags=['연금'])
    def get(self, request, product_pk):
        product = get_object_or_404(PensionProduct, pk=product_pk)
        product_serializer = PensionProductSerializer(product)
        return JsonResponse(product_serializer.data)

# 전세대출 --------------------------------------------------------
class RentLoanProductRegisterAPIView(APIView):
    url = f'http://finlife.fss.or.kr/finlifeapi/rentHouseLoanProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'

    @swagger_auto_schema(
        operation_summary="외부 API에서 전,월세 보증금 대출 상품 정보를 가져와 데이터베이스에 저장합니다.",
        tags=['대출']
    )
    def get(self, request):
        response = requests.get(self.url).json()
        product_list = response.get('result', {}).get('baseList', [])
        option_list = response.get('result', {}).get('optionList', [])

        # 전세대출 상품 정보를 가져와 데이터베이스에 저장합니다.
        for product_data in product_list:
            fin_prdt_cd = product_data.get('fin_prdt_cd')
            # 중복 확인
            if not RentLoanProduct.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
                fin_co_no = product_data.get('fin_co_no')
                fin_co_instance = Bank.objects.get(fin_co_no=fin_co_no)
                serializer = RentLoanSerializer(data=product_data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(fin_co_no=fin_co_instance)

        # 전세대출 상품 옵션 정보를 가져와 데이터베이스에 저장합니다.
        for option_data in option_list:
            fin_prdt_cd = option_data.get('fin_prdt_cd')
            product = RentLoanProduct.objects.get(fin_prdt_cd=fin_prdt_cd)
            serializer = RentLoanOptionSerializer(data=option_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(rent_loan_product=product)

        return JsonResponse({"message": "전세대출 상품 정보가 성공적으로 저장되었습니다."}, status=201)
    
class RentLoanDetailAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="전월세보증금대출 상품의 상세 정보를 가져옵니다.",
        tags=['대출']
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
        tags=['금융'],
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

            user_product_data = {
                'user': request.user.pk,
                'product_type': product_type,
                'selected_option': option.pk,
                'join_date': timezone.now().date()
            }

            print(f'user_product_data: {user_product_data}')

            if product_type == '정기예금':
                user_product_data['deposit_product'] = product.pk
                user_product_serializer = UserDepositProductSerializer(data=user_product_data)
            elif product_type == '적금':
                user_product_data['saving_product'] = product.pk
                user_product_serializer = UserSavingProductSerializer(data=user_product_data)
            elif product_type == '연금':
                user_product_data['pension_product'] = product.pk
                user_product_serializer = UserPensionProductSerializer(data=user_product_data)
            elif product_type == '전세대출':
                user_product_data['rent_loan_product'] = product.pk
                user_product_serializer = UserRentLoanProductSerializer(data=user_product_data)
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
        print(f'product: {product}, option: {option}')
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
    

# 각 금융 상품 리스트 API View
class DepoistProductListAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="정기 예금 상품 리스트를 가져옵니다.",
        tags=['정기예금']
    )
    def get(self, request):
        deposit_products = DepositProduct.objects.all()
        serializer = DepositListSerializer(deposit_products, many=True)
        return JsonResponse(serializer.data, safe=False)

class SavingProductListAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="적금 상품 리스트를 가져옵니다.",
        tags=['적금']
    )
    def get(self, request):
        saving_products = SavingProduct.objects.all()
        serializer = SavingListSerializer(saving_products, many=True)
        return JsonResponse(serializer.data, safe=False)

class PensionProductListAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="연금 상품 리스트를 가져옵니다.",
        tags=['연금']
    )
    def get(self, request):
        pension_products = PensionProduct.objects.all()
        serializer = PensionListSerializer(pension_products, many=True)
        return JsonResponse(serializer.data, safe=False)

class RentLoanProductListAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="전세대출 상품 리스트를 가져옵니다.",
        tags=['대출']
    )
    def get(self, request):
        rent_loan_products = RentLoanProduct.objects.all()
        serializer = RentLoanListSerializer(rent_loan_products, many=True)
        return JsonResponse(serializer.data, safe=False)