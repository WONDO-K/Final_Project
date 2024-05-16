from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model() # accounts.User

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles') # 게시글 작성자

class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes') # 좋아요를 누른 게시글
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes') # 좋아요를 누른 유저

class Comment(models.Model):
    content = models.TextField(max_length=200) # 댓글 내용
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments') # 댓글이 달린 게시글
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments') # 댓글 작성자

