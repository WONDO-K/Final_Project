import random
import json
from collections import OrderedDict
from django.core.wsgi import get_wsgi_application
from django.utils import timezone

# Django 프로젝트 설정 파일 경로 설정
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewBee.settings')
application = get_wsgi_application()

from accounts.models import User  # User 모델 임포트
from products.models import DepositProduct, SavingProduct, PensionProduct, RentLoanProduct  # 금융 상품 모델 임포트
from products.models import DepositProductOption, SavingProductOption, PensionProductOption, RentLoanProductOption  # 금융 상품 옵션 모델 임포트
from products.models import UserDepositProduct, UserSavingProduct, UserPensionProduct, UserRentLoanProduct  # 중계 테이블 모델 임포트

# 샘플 한글 이름
first_name_samples = '김이박최정강조윤장임'
middle_name_samples = '민서예지도하주윤채현지'
last_name_samples = '준윤우원호후서연아은진'

# 랜덤한 사용자 이름 생성
def random_username():
    length = random.randint(3, 30)
    letters_and_digits = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))


# 랜덤한 이름 생성
def random_name():
    result = ''
    result += random.choice(first_name_samples)
    result += random.choice(middle_name_samples)
    result += random.choice(last_name_samples)
    return result + str(random.randint(1, 100))

# 데이터 생성
N = 10000
username_list = []
for _ in range(N):
    while True:
        rn = random_name()
        if rn not in username_list:
            username_list.append(rn)
            break

# 저장 위치는 프로젝트 구조에 맞게 수정합니다.
user_save_dir = 'accounts/fixtures/accounts/user_data.json'

# 사용자 데이터 및 금융 상품 생성 및 연결
with open(user_save_dir, 'w', encoding="utf-8") as f:
    f.write('[')

    for i in range(N):
        file = OrderedDict()
        # 모델과 pk 설정
        file['model'] = 'accounts.User'
        file['pk'] = i + 1
        # 필드 설정
        file['fields'] = {
            'username': random_username(),  # 랜덤한 사용자 이름 생성
            'nickname': None,  # 닉네임
            'email': f'{username_list[i]}@example.com',  # 이메일
            'age': random.randint(1, 100),  # 나이
            'money': random.randrange(0, 100000000, 100000),  # 현재 가진 금액
            'salary': random.randrange(0, 1500000000, 1000000),  # 연봉
            'financial_products': '',  # 중계 테이블로 대체
            'is_active': True,  # 계정 활성화 상태
            'is_staff': False,  # 스태프 여부
            'is_superuser': False,  # 슈퍼유저 여부
        }

        # 유저 저장
        json.dump(file, f, ensure_ascii=False, indent=4)
        if i != N - 1:
            f.write(',')

        # 더미 금융 상품 정보 생성
        product_count = random.randint(0, 5)  # 사용자당 0~5개의 금융 상품 생성
        for _ in range(product_count):
            product_type = random.choice(['deposit', 'saving', 'pension', 'rent_loan'])
            if product_type == 'deposit':
                product = random.choice(DepositProduct.objects.all())
                option = random.choice(DepositProductOption.objects.all())
                join_date = timezone.now()  # 현재 시간으로 설정
                user_product = UserDepositProduct(user_id=i + 1, deposit_product=product, selected_option=option, join_date=join_date)
            elif product_type == 'saving':
                product = random.choice(SavingProduct.objects.all())
                option = random.choice(SavingProductOption.objects.all())
                join_date = timezone.now()  # 현재 시간으로 설정
                user_product = UserSavingProduct(user_id=i + 1, saving_product=product, selected_option=option, join_date=join_date)
            elif product_type == 'pension':
                product = random.choice(PensionProduct.objects.all())
                option = random.choice(PensionProductOption.objects.all())
                join_date = timezone.now()  # 현재 시간으로 설정
                user_product = UserPensionProduct(user_id=i + 1, pension_product=product, selected_option=option, join_date=join_date)
            elif product_type == 'rent_loan':
                product = random.choice(RentLoanProduct.objects.all())
                option = random.choice(RentLoanProductOption.objects.all())
                join_date = timezone.now()  # 현재 시간으로 설정
                user_product = UserRentLoanProduct(user_id=i + 1, rent_loan_product=product, selected_option=option, join_date=join_date)
            user_product.save()

    f.write(']')
    print(f'{N}개 사용자 데이터 생성 및 연결 완료 / 저장 위치: {user_save_dir}')

print(f'사용자 데이터 생성 및 연결 완료 / 저장 위치: {user_save_dir}')