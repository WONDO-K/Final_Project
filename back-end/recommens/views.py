import numpy as np
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView
from products.models import UserDepositProduct, UserSavingProduct, UserPensionProduct, UserRentLoanProduct
from products.models import DepositProduct, SavingProduct, PensionProduct, RentLoanProduct
from drf_yasg.utils import swagger_auto_schema

class TopProductsView(APIView):
    @swagger_auto_schema(
        operation_summary='Top 5 products',
        tags=['Top Products'],
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
