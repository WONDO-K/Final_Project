from rest_framework import serializers
from django.contrib.auth.models import User # User 모델
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password # Django의 기본 pw 검증 도구
from rest_framework.validators import UniqueValidator # 이메일 중복 방지를 위한 검증 도구
from datetime import date
from django.contrib.auth import authenticate


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())], # 이메일에 대한 중복 검증
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password], # 비밀번호에 대한 검증
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
                {"password": "Password fields didn't match."})
        
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

class LoginSerializer(serializers.Serializer):
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