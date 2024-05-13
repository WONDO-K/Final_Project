from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'user_name', 'nick_name', 'email', 'birth', 'age', 'salary', 'gender', 'wealth', 'is_staff', 'my_product']

    def create(self, validated_data):
        user_id = validated_data.get('user_id')
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User(
            user_id=user_id,
            email=email
        )
        user.set_password(password)
        user.save()
        return user
