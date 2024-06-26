from django.urls import path
from .views import *

app_name = 'products'

urlpatterns = [
    # 은행 정보 
    path('banks/', BankRegisterAPIView.as_view(), name='bank-register'),
    path('banks/<int:bank_pk>/', BankDetailAPIView.as_view(), name='bank-detail'),
    path('banks/products/<int:bank_pk>/', BanksProductsAPIView.as_view(), name='bank-product-list'),

    # 정기 예금
    path('deposit/register/', DepositProductRegisterAPIView.as_view(), name='product-register'),
    path('deposit/<int:product_pk>/', DepositProductDetailAPIView.as_view(), name='product-detail'),

    # 적금
    path('saving/register/', SavingProductRegisterAPIView.as_view(), name='saving-register'),
    path('saving/<int:product_pk>/', SavingProductDetailAPIView.as_view(), name='saving-detail'),

    # 연금
    path('pension/register/', PensionProductRegisterAPIView.as_view(), name='pension-register'),
    path('pension/<int:product_pk>/', PensionProductDetailAPIView.as_view(), name='pension-detail'),

    # 전월세보증금대출
    path('rent-loan/register/', RentLoanProductRegisterAPIView.as_view(), name='rent-loan-register'),
    path('rent-loan/<int:product_pk>/', RentLoanDetailAPIView.as_view(), name='rent-loan-detail'),

    # 상품 가입
    path("join_product/", JoinProductAPIView.as_view(), name='join_product'),

    # 상품 리스트 조회
    path("deposit_list/", DepoistProductListAPIView.as_view(), name='deposit-list'),
    path("saving_list/", SavingProductListAPIView.as_view(), name='saving-list'),
    path("pension_list/", PensionProductListAPIView.as_view(), name='pension-list'),
    path("rent_loan_list/", RentLoanProductListAPIView.as_view(), name='rent-loan-list'),
    
    # 적금 만기 시 예상 수령액
    path('calculate_maturity_amount/', CalculateEndSavingAmountAPIView.as_view(), name='calculate_maturity_amount'),

]
