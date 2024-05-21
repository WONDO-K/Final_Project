import random
import json
from collections import OrderedDict
from django.core.wsgi import get_wsgi_application

# Django 프로젝트 설정 파일 경로 설정
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewBee.settings')
application = get_wsgi_application()

from accounts.models import User  # User 모델 임포트
from products.models import DepositProduct, SavingProduct, PensionProduct, RentLoanProduct  # 금융 상품 모델 임포트
from products.models import DepositProductOption, SavingProductOption, PensionProductOption, RentLoanProductOption  # 금융 상품 옵션 모델 임포트
from products.models import UserDepositProduct, UserSavingProduct, UserPensionProduct, UserRentLoanProduct  # 중계 테이블 모델 임포트

N = 10000

# 금융 상품 목록 조회
financial_products = {
    'deposit': list(DepositProduct.objects.all()),
    'saving': list(SavingProduct.objects.all()),
    'pension': list(PensionProduct.objects.all()),
    'rent_loan': list(RentLoanProduct.objects.all()),
}

# 금융 상품 옵션 목록 조회
financial_options = {
    'deposit': list(DepositProductOption.objects.all()),
    'saving': list(SavingProductOption.objects.all()),
    'pension': list(PensionProductOption.objects.all()),
    'rent_loan': list(RentLoanProductOption.objects.all()),
}

# 저장 위치는 프로젝트 구조에 맞게 수정합니다.
user_product_save_dir = 'accounts/fixtures/accounts/user_product_data.json'

# 중계 테이블 데이터 생성
with open(user_product_save_dir, 'w', encoding="utf-8") as f:
    f.write('[')

    user_id = 1
    for user in User.objects.all():
        product_count = random.randint(0, 5) # 0 ~ 5개의 금융 상품을 가입
        user_products = random.choices(list(financial_products.keys()), k=product_count) # 가입할 금융 상품 종류 랜덤 선택
        print(f'financial_products: {financial_products}')
        print(f'financial_options: {financial_options}')
        for product_type in user_products:
            product = random.choice(financial_products[product_type]) # 가입할 금융 상품 랜덤 선택
            option = random.choice(financial_options[product_type]) # 가입할 금융 상품 옵션 랜덤 선택
            join_date = f'{random.randint(2015, 2023)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}'

            if product_type == 'deposit':
                model = 'financial.UserDepositProduct'
                user_product = UserDepositProduct(user=user, product_type=product_type, deposit_product=product, selected_option=option, join_date=join_date)
            elif product_type == 'saving':
                model = 'financial.UserSavingProduct'
                user_product = UserSavingProduct(user=user, product_type=product_type, saving_product=product, selected_option=option, join_date=join_date)
            elif product_type == 'pension':
                model = 'financial.UserPensionProduct'
                user_product = UserPensionProduct(user=user, product_type=product_type, pension_product=product, selected_option=option, join_date=join_date)
            elif product_type == 'rent_loan':
                model = 'financial.UserRentLoanProduct'
                user_product = UserRentLoanProduct(user=user, product_type=product_type, rent_loan_product=product, selected_option=option, join_date=join_date)

            file = OrderedDict()
            file['model'] = model
            file['pk'] = user_id
            file['fields'] = {
                'user': user.pk,
                'product_type': product_type,
                'deposit_product' if product_type == 'deposit' else 'saving_product' if product_type == 'saving' else 'pension_product' if product_type == 'pension' else 'rent_loan_product': product.pk,
                'selected_option': option.pk,
                'join_date': join_date
            }
            
            json.dump(file, f, ensure_ascii=False, indent=4)
            user_id += 1
            if user_id != N - 1:
                f.write(',')
    f.write(']')

print(f'중계 테이블 데이터 생성 완료 / 저장 위치: {user_product_save_dir}')