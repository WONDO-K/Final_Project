from rest_framework import serializers
from .models import Article, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','content', 'user', 'article']
        read_only_fields = ['id','user', 'article']  # user,article 읽기 전용으로 유지

    def create(self, validated_data):
        return super().create(validated_data)


class ArticleSerializer(serializers.ModelSerializer):
  comments = CommentSerializer(many=True, read_only=True)

  class Meta:
        model = Article
        fields = ['id','title', 'content', 'user', 'comments']
        read_only_fields = ['id','user', 'comments']

