from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Article, Comment

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()  # 수정된 부분

    class Meta:
        model = User
        fields = ['id', 'username']  # username을 포함시킴

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'article']
        read_only_fields = ['id', 'user', 'article']

    def create(self, validated_data):
        return super().create(validated_data)


class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'user', 'comments']
        read_only_fields = ['id', 'user', 'comments']

