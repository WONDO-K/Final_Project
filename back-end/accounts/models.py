from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin,BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, user_id, password=None, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수 항목입니다.')
        if not user_id:
            raise ValueError('사용자 ID는 필수 항목입니다.')
        
        email = self.normalize_email(email)
        user = self.model(email=email, user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('슈퍼유저는 is_staff=True 여야 합니다.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('슈퍼유저는 is_superuser=True 여야 합니다.')

        return self.create_user(email, user_id, password, **extra_fields)

class User(AbstractUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('남자', '남자'),
        ('여자', '여자'),
    ]
    user_id = models.CharField(max_length=20, unique=True)
    user_name = models.CharField(max_length=20)
    nick_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50, unique=True)
    birth = models.DateTimeField()
    age = models.IntegerField()
    salary = models.IntegerField()
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, null=True, blank=True)
    wealth = models.IntegerField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    my_product = models.JSONField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_id']

    class Meta:
        db_table = 'user'