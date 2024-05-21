import random
import json
from collections import OrderedDict
import string
from django.core.wsgi import get_wsgi_application
from django.utils import timezone
from datetime import datetime, timedelta

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

# 랜덤한 이름 생성
def random_name():
    result = ''
    result += random.choice(first_name_samples)
    result += random.choice(middle_name_samples)
    result += random.choice(last_name_samples)
    return result 

# 데이터 생성
N = 10000
# 이름 리스트 생성
realname_list = [random_name() for _ in range(N)]

# 저장 위치는 프로젝트 구조에 맞게 수정합니다.
user_save_dir = 'accounts/fixtures/accounts/user_data.json'

# 생년월일 범위 설정
start_date = datetime(1930, 1, 1)
end_date = datetime(2010, 12, 31)

# 랜덤한 생년월일 생성 함수
def random_birth(start_date, end_date):
    random_birth_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_birth_date.strftime('%Y-%m-%d')

# 나이 계산 함수
def calculate_age(birth_date):
    today = datetime.today()
    birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


# 사용자 데이터 및 금융 상품 생성 및 연결
with open(user_save_dir, 'w', encoding="utf-8") as f:
    f.write('[')

    for i in range(N):

        username = f'dummy{i+1}'  # 규칙을 가진 아이디 생성
        birth = random_birth(start_date, end_date)
        file = OrderedDict()
        # 모델과 pk 설정
        file['model'] = 'accounts.User'
        file['pk'] = i + 1
        # 필드 설정
        file['fields'] = {
            'username': username,  # 랜덤한 사용자 이름 생성
            'realname': realname_list[i],  # 유저 이름 랜덤 생성
            'password': 'Qwe123123!',  # 비밀번호
            'nickname': username,  # 닉네임
            'email': f'{username}@example.com',  # 이메일
            'wealth': random.randrange(0, 100000000, 100000),  # 현재 가진 금액
            'salary': random.randrange(0, 150000000, 1000000),  # 연봉
            'birth' : birth,  # 랜덤한 생년월일 생성
            'age': calculate_age(birth),  # 나이 계산
            'date_joined': f'{random.randint(2015, 2023)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}',  # 가입일
            'is_active': True,  # 계정 활성화 상태
            'is_staff': False,  # 스태프 여부
            'is_superuser': False,  # 슈퍼유저 여부
        }

        # 유저 저장
        json.dump(file, f, ensure_ascii=False, indent=4)
        if i != N - 1:
            f.write(',')

    f.write(']')
    print(f'{N}개 사용자 데이터 생성 및 연결 완료 / 저장 위치: {user_save_dir}')

