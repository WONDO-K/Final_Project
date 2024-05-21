from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin,BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수 항목입니다.')
        if not username:
            raise ValueError('사용자 ID는 필수 항목입니다.')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('슈퍼유저는 is_staff=True 여야 합니다.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('슈퍼유저는 is_superuser=True 여야 합니다.')

        return self.create_user(email, username, password, **extra_fields)

class User(AbstractUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('남자', '남자'),
        ('여자', '여자'),
    ]
    # 안전상의 이유로 Swagger에서는 password를 제외하고 보여준다.
    # 그래서 Swagger에서 password를 제외하고 보여주기 위해 아래와 같이 작성한다.
    # 또한 Swagger에서 회원가입 시에는 password를 입력하여 회원가입을 할 수 있도록 처리했음.
    # user_id = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=20, unique=True) # user_id -> username으로 변경
    realname = models.CharField(max_length=20,null=False) # user_name -> real_name으로 변경
    nickname = models.CharField(max_length=20,null=False)
    email = models.EmailField(max_length=50, unique=True)
    birth = models.DateField(null=False) # DateTimeField-> DateField으로 변경 (생년월일만 입력받기 위함)
    age = models.IntegerField(null=False)
    salary = models.IntegerField(null=False)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, null=True, blank=True)
    wealth = models.IntegerField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    #my_product = models.JSONField(null=True, blank=True)
    objects = UserManager()
    
    USERNAME_FIELD = 'username' # email로 로그인하는 것이 아닌 user_id로 로그인하기 위함
    REQUIRED_FIELDS = ['email'] # 사용자가 회원가입 시에 필수로 입력해야 하는 필드

    class Meta:
        db_table = 'user'