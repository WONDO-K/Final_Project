from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Article, Comment

User = get_user_model()


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
    comments = serializers.SerializerMethodField()  # 댓글을 직렬화하기 위해 SerializerMethodField 사용

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'user', 'comments', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'comments']

    def get_user(self, obj):
        return obj.user.username  # 게시글 작성자의 username 반환
    
    def get_comments(self, obj):
        comments = obj.comments.all()  # 해당 게시글의 모든 댓글을 가져옴
        return [
            {
                'id': comment.id,
                'content': comment.content,
                'user': comment.user.username,
                'article': obj.id  # 게시글의 ID를 사용
            }
            for comment in comments
        ]
    
class ArticleListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()  # UserSerializer 대신 SerializerMethodField 사용

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'user', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user']

    def get_user(self, obj):
        return obj.user.username  # 게시글 작성자의 username 반환