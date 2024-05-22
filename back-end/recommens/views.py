import numpy as np
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView
from products.models import UserDepositProduct, UserSavingProduct, UserPensionProduct, UserRentLoanProduct
from products.models import DepositProduct, SavingProduct, PensionProduct, RentLoanProduct
from drf_yasg.utils import swagger_auto_schema
from accounts.models import User


class TopProductsView(APIView):
    @swagger_auto_schema(
        operation_summary='상품별 가입자 수 Top 5',
        tags=['상품 추천'],
    )
    def get(self, request):
        top_products = self.get_top_5_products()
        return Response(top_products)

    def get_top_5_products(self):
        # 예금 상품 Top 5
        deposit_top_5 = (
            UserDepositProduct.objects.values('deposit_product')
            .annotate(count=Count('user'))
            .order_by('-count')[:5]
        )

        # 적금 상품 Top 5
        saving_top_5 = (
            UserSavingProduct.objects.values('saving_product')
            .annotate(count=Count('user'))
            .order_by('-count')[:5]
        )

        # 연금 상품 Top 5
        pension_top_5 = (
            UserPensionProduct.objects.values('pension_product')
            .annotate(count=Count('user'))
            .order_by('-count')[:5]
        )

        # 대출 상품 Top 5
        rent_loan_top_5 = (
            UserRentLoanProduct.objects.values('rent_loan_product')
            .annotate(count=Count('user'))
            .order_by('-count')[:5]
        )
        def convert_to_list(queryset, product_type):
            # 상품 모델에 따라 필요한 속성을 선택합니다.
            if product_type == 'deposit':
                product_model = DepositProduct
            elif product_type == 'saving':
                product_model = SavingProduct
            elif product_type == 'pension':
                product_model = PensionProduct
            elif product_type == 'rent_loan':
                product_model = RentLoanProduct

            # 각 상품의 id와 fin_prdt_nm, 그리고 count를 포함하여 반환합니다.
            return [{'id': item[f'{product_type}_product'], 'name': product_model.objects.get(pk=item[f'{product_type}_product']).fin_prdt_nm, 'count': item['count']} for item in queryset]

        deposit_top_5_list = convert_to_list(deposit_top_5, 'deposit')
        saving_top_5_list = convert_to_list(saving_top_5, 'saving')
        pension_top_5_list = convert_to_list(pension_top_5, 'pension')
        rent_loan_top_5_list = convert_to_list(rent_loan_top_5, 'rent_loan')

        return {
            'deposit': deposit_top_5_list,
            'saving': saving_top_5_list,
            'pension': pension_top_5_list,
            'rent_loan': rent_loan_top_5_list,
        }
    
from drf_yasg import openapi
from .serializers import RecommendProductsQuerySerializer


class SimmilarRecommendProductsAPIView(APIView):
    @swagger_auto_schema(
        operation_summary='사용자 정보를 기반으로 상위 제품을 추천합니다.',
        tags=['상품 추천'],
        query_serializer=RecommendProductsQuerySerializer
    )
    def get(self,request):
        serializer = RecommendProductsQuerySerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        age = serializer.validated_data['age']
        wealth = serializer.validated_data['wealth']
        salary = serializer.validated_data['salary']

        # 범위 설정
        age_range = 5
        wealth_range = 10_000_000
        salary_range = 1_000_000

        # 범위 내에서 유사한 사용자들의 상품 가입 정보를 가져온다..
        similar_users = self.find_similar_users(age, wealth, salary, age_range, wealth_range, salary_range)

        # 각 상품별로 가입자 수를 계산한다.
        product_counts = self.calculate_product_counts(similar_users)

        # 가입자 수를 기준으로 상위 3개 상품을 추출한다.
        top_products = self.extract_top_products(product_counts)

        return Response(top_products)
    
    def find_similar_users(self, age, wealth, salary, age_range, wealth_range, salary_range):
        min_age = age - age_range # 최소 나이
        max_age = age + age_range # 최대 나이
        min_wealth = wealth - wealth_range # 최소 자산
        max_wealth = wealth + wealth_range # 최대 자산
        min_salary = salary - salary_range # 최소 연봉
        max_salary = salary + salary_range # 최대 연봉

        # 범위 내에서 유사한 사용자들의 상품 가입 정보를 필터링.
        similar_users = User.objects.filter(
            age__range=(min_age, max_age),
            wealth__range=(min_wealth, max_wealth),
            salary__range=(min_salary, max_salary)
        )
        return similar_users

    # def calculate_product_counts(self, users):
    #     # 각 상품별 가입자 수를 계산
    #     deposit_counts = UserDepositProduct.objects.filter(user__in=users).values('deposit_product').annotate(count=Count('user'))
    #     saving_counts = UserSavingProduct.objects.filter(user__in=users).values('saving_product').annotate(count=Count('user'))
    #     pension_counts = UserPensionProduct.objects.filter(user__in=users).values('pension_product').annotate(count=Count('user'))
    #     rent_loan_counts = UserRentLoanProduct.objects.filter(user__in=users).values('rent_loan_product').annotate(count=Count('user'))

    #     return deposit_counts, saving_counts, pension_counts, rent_loan_counts
    
    def calculate_product_counts(self, users):
        # 각 상품별 가입자 수를 계산
        deposit_counts = UserDepositProduct.objects.filter(user__in=users).values('deposit_product', 'deposit_product__fin_prdt_nm').annotate(count=Count('user'))
        saving_counts = UserSavingProduct.objects.filter(user__in=users).values('saving_product', 'saving_product__fin_prdt_nm').annotate(count=Count('user'))
        pension_counts = UserPensionProduct.objects.filter(user__in=users).values('pension_product', 'pension_product__fin_prdt_nm').annotate(count=Count('user'))
        rent_loan_counts = UserRentLoanProduct.objects.filter(user__in=users).values('rent_loan_product', 'rent_loan_product__fin_prdt_nm').annotate(count=Count('user'))

        return deposit_counts, saving_counts, pension_counts, rent_loan_counts

    def extract_top_products(self, product_counts):
        # 상품별 가입자 수를 기준으로 상위 3개 상품을 추출합니다.
        top_deposit_products = sorted(product_counts[0], key=lambda x: x['count'], reverse=True)[:3]
        top_saving_products = sorted(product_counts[1], key=lambda x: x['count'], reverse=True)[:3]
        top_pension_products = sorted(product_counts[2], key=lambda x: x['count'], reverse=True)[:3]
        top_rent_loan_products = sorted(product_counts[3], key=lambda x: x['count'], reverse=True)[:3]

        return {
            'deposit': top_deposit_products,
            'saving': top_saving_products,
            'pension': top_pension_products,
            'rent_loan': top_rent_loan_products,
        }