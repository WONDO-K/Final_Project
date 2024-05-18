from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Article, Comment

User = get_user_model()

# class UserSerializer(serializers.ModelSerializer):
#     username = serializers.CharField()  # 수정된 부분

#     class Meta:
#         model = User
#         fields = ['id', 'username']  # username을 포함시킴
#         read_only_fields = ['id', 'username']  # 수정된 부분
#         ref_name = 'ArticleUserSerializer'  # ref_name 추가

# class CommentSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)

#     class Meta:
#         model = Comment
#         fields = ['id', 'content', 'user', 'article']
#         read_only_fields = ['id', 'user', 'article']

#     def create(self, validated_data):
#         return super().create(validated_data)


# class ArticleSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     comments = CommentSerializer(many=True, read_only=True)

#     class Meta:
#         model = Article
#         fields = ['id', 'title', 'content', 'user', 'comments', 'created_at', 'updated_at']
#         read_only_fields = ['id', 'user', 'comments']
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()  # UserSerializer 대신 SerializerMethodField 사용

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'article']
        read_only_fields = ['id', 'user', 'article']

    def get_user(self, obj):
        return obj.user.username  # 댓글 작성자의 username 반환

    def create(self, validated_data):
        return super().create(validated_data)


class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()  # UserSerializer 대신 SerializerMethodField 사용

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'user', 'comments', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'comments']

    def get_user(self, obj):
        return obj.user.username  # 게시글 작성자의 username 반환