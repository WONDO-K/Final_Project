import random
import json
from collections import OrderedDict
from django.core.wsgi import get_wsgi_application

# Django 프로젝트 설정 파일 경로 설정
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewBee.settings')
application = get_wsgi_application()

from accounts.models import User
from products.models import DepositProduct, SavingProduct, PensionProduct, RentLoanProduct
from products.models import DepositProductOption, SavingProductOption, PensionProductOption, RentLoanProductOption
from products.models import UserDepositProduct, UserSavingProduct, UserPensionProduct, UserRentLoanProduct

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

# 각 모델별 pk 초기값 설정
user_deposit_product_id = 1
user_saving_product_id = 1
user_pension_product_id = 1
user_rent_loan_product_id = 1

# 저장 위치는 프로젝트 구조에 맞게 수정합니다.
user_product_save_dir = 'accounts/fixtures/accounts/user_product_data.json'

# 중계 테이블 데이터 생성
with open(user_product_save_dir, 'w', encoding="utf-8") as f:
    f.write('[')
    first_record = True  # 첫 번째 레코드 여부 확인용 플래그
    for user in User.objects.all():
        product_count = random.randint(1, 5)  # 1 ~ 5개의 금융 상품을 가입
        user_products = random.choices(list(financial_products.keys()), k=product_count)  # 가입할 금융 상품 종류 랜덤 선택
        user_product_set = set()  # 중복 방지를 위한 사용자 상품 세트
        for product_type in user_products:
            product_list = financial_products[product_type]
            # 사용자가 가입한 금융 상품 제외한 상품 리스트
            available_products = [product for product in product_list if (user.pk, product.pk) not in user_product_set]

            if not available_products:
                continue

            product = random.choice(available_products)  # 가입할 금융 상품 랜덤 선택
            # 유저pk와 상품pk를 튜플로 묶어 사용자 상품 세트에 추가
            # 현재 유저가 상품 가입을 진행 중일 때 중복 가입을 추적할 수 있도록 함
            user_product_set.add((user.pk, product.pk)) # 중복 방지를 위해 사용자 상품 세트에 추가

            options = financial_options[product_type]  # 해당 상품의 옵션들
            option = random.choice(options) if options else None  # 가입할 금융 상품 옵션 랜덤 선택
            join_date = f'{random.randint(2015, 2023)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}'

            if product_type == 'deposit':
                model = 'products.UserDepositProduct'
                pk = user_deposit_product_id
                user_deposit_product_id += 1
            elif product_type == 'saving':
                model = 'products.UserSavingProduct'
                pk = user_saving_product_id
                user_saving_product_id += 1
            elif product_type == 'pension':
                model = 'products.UserPensionProduct'
                pk = user_pension_product_id
                user_pension_product_id += 1
            elif product_type == 'rent_loan':
                model = 'products.UserRentLoanProduct'
                pk = user_rent_loan_product_id
                user_rent_loan_product_id += 1

            file = OrderedDict()
            file['model'] = model
            file['pk'] = pk
            file['fields'] = {
                'user': user.pk,
                'product_type': product_type,
                # 상품 종류에 따라 다른 모델의 pk를 저장
                'deposit_product' if product_type == 'deposit' else 'saving_product' if product_type == 'saving' else 'pension_product' if product_type == 'pension' else 'rent_loan_product': product.pk,
                'selected_option': option.pk if option else None,
                'join_date': join_date
            }

            if not first_record:
                f.write(',')
            else:
                first_record = False

            json.dump(file, f, ensure_ascii=False, indent=4)
    f.write(']')