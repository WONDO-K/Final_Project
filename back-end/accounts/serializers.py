from rest_framework import serializers
from django.contrib.auth.models import User # User 모델
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password # Django의 기본 pw 검증 도구
from rest_framework.validators import UniqueValidator # 이메일 중복 방지를 위한 검증 도구
from datetime import date
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
import re

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        required=True,
        validators = [
            UniqueValidator(queryset=User.objects.all()), # 아이디에 대한 중복 검증
            RegexValidator(
                regex=r'^[a-z0-9]{3,30}$',
                message='아이디는 3~30자의 영문 소문자, 숫자로 이루어져야 합니다.',
            )
        ]
    )

    email = serializers.EmailField( # 이메일은 EmailField가 자동으로 정규식을 검증한다.
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())], # 이메일에 대한 중복 검증
    )
    password = serializers.CharField( # 비밀번호에 대한 검증
        write_only=True,
        required=True,
    )
    
    password2 = serializers.CharField( # 비밀번호 확인을 위한 필드
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = ['username', 'realname', 'password', 'password2', 'nickname', 'email', 'birth', 'salary', 'gender', 'wealth', 'is_staff', 'my_product']   

    def validate(self, data): # password과 password2의 일치 여부 확인
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "비밀번호가 확인용 비밀번호와 일치하지 않습니다."})
        
        # 비밀번호 유효성 검사 추가
        password = data['password']
        print(f'password: {password}')
        print(f'password2 : {data["password2"]}')
        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()-_=+])[a-zA-Z\d!@#$%^&*()-_=+]{8,}$'  # 최소 8자, 하나 이상의 소문자, 대문자, 숫자 포함
        if not re.match(password_regex, password):
            raise serializers.ValidationError("비밀번호는 8자 이상이어야 하며, 최소 1개의 숫자, 대문자, 소문자, 특수문자를 포함해야 합니다.")
        
        return data

    def create(self, validated_data):
        validated_data.pop('password2', None)  # password2 필드 제거 (User 모델에는 존재하지 않음, 일치 여부를 확인하기 위한 용도로만 사용했기 때문에 저장할 필요가 없음.)
        password = validated_data.pop('password') # password 필드를 따로 저장하고 validated_data에서는 제거한다. 이유는 구현안 커스텀 User 모델에는 password가 없기 때문이다.
        birth = validated_data.get('birth')
        today = date.today()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))  # 만 나이 계산
        validated_data['age'] = age
        user = User.objects.create_user(password=password, **validated_data) # 패스워드는 해싱처리가 자동으로 된다.(Django의 기본 User 모델의 create_user 메서드를 사용하여 생성한다.)
        return user
        # user_id = validated_data.get('user_id')
        # email = validated_data.get('email')
        # password = validated_data.get('password')
        # user_name = validated_data.get('user_name')
        # nick_name = validated_data.get('nick_name')
        # birth = validated_data.get('birth')
        # age = validated_data.get('age')
        # salary = validated_data.get('salary')
        # gender = validated_data.get('gender')
        # wealth = validated_data.get('wealth')
        # user = User(
        #     user_id=user_id,
        #     email=email,
        #     user_name=user_name,
        #     nick_name=nick_name,
        #     birth=birth,
        #     age=age,
        #     salary=salary,
        #     gender=gender,
        #     wealth=wealth
        # )
        # user.set_password(password)
        # user.save()
        # return user

# 로그인
class LoginSerializer(serializers.Serializer): # 로그인은 DB와 관련이 없기 때문에 ModelSerializer가 아닌 Serializer를 사용한다.
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("사용자 정보가 올바르지 않습니다.")
        else:
            raise serializers.ValidationError("아이디와 비밀번호를 입력해주세요.")
        return {
            'user': user,
            'username': user.username,
            'user_id': user.pk,
        }

# 회원 정보 수정
class UserUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['nickname', 'email', 'salary', 'gender', 'wealth'] # 수정 가능한 필드만 넣어준다.
        read_only_fields = ['username', 'email','access_token','refresh_token',]
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None) # 보안상 passwrod는 setattr로 변경하면 안되기 때문에 일단 빼놓는다.
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password) # 빼놓은 password를 여기서 변경한다.
        instance.save()
        return instance

# 비밀번호 변경
class ChangePasswordSerializer(serializers.ModelSerializer):
    # write_only=True : 사용자에게 입력받아 서버에서만 사용할 수 있도록 하는 옵션
    # 직렬화된 출력에서 제외하고 싶은 필드에는 write_only=True를 사용한다.
    # 클라이언트에게 비밀번호가 노출되지 않도록 하기 위함
    # required=True : 필수 입력값
    old_password = serializers.CharField(write_only=True, required=True) # 기존 비밀번호
    new_password = serializers.CharField(write_only=True, required=True) # 새로운 비밀번호
    new_password2 = serializers.CharField(write_only=True, required=True) # 새로운 비밀번호 확인

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'new_password2']

    def validate(self, data):
        user = self.context['request'].user
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        new_password2 = data.get('new_password2')

        # 기존 비밀번호가 올바른지 확인
        if not authenticate(username=user.username, password=old_password):
            raise serializers.ValidationError("기존 비밀번호가 올바르지 않습니다.")
        # 새로운 비밀번호와 기존 비밀번호가 일치하는지 확인
        if old_password == new_password:
            raise serializers.ValidationError("새로운 비밀번호는 기존 비밀번호와 다르게 설정해야 합니다.")
        # 새로운 비밀번호와 비밀번호 확인이 일치하는지 확인
        if new_password != new_password2:
            raise serializers.ValidationError("새로운 비밀번호가 일치하지 않습니다.")

        # 새로운 비밀번호의 정규식 유효성 검사 추가
        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()-_=+])[a-zA-Z\d!@#$%^&*()-_=+]{8,}$'  # 최소 8자, 하나 이상의 소문자, 대문자, 숫자, 특수문자 포함
        if not re.match(password_regex, new_password):
            raise serializers.ValidationError("비밀번호는 8자 이상이어야 하며, 최소 1개의 숫자, 대문자, 소문자, 특수문자를 포함해야 합니다.")

        return data

    def save(self, user):
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user