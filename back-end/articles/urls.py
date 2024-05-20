from django.urls import path
from .views import ArticleListCreateAPIView, ArticleRetrieveAPIView, CommentCreateAPIView, CommentRetrieveAPIView, ArticleLikesAPIView

app_name = 'articles'

urlpatterns = [
    # Articles
    path('articles/', ArticleListCreateAPIView.as_view(), name='article-list-create'),
    path('articles/<int:pk>/', ArticleRetrieveAPIView.as_view(), name='article-retrieve'),

    # Article Likes
    path('articles/<int:pk>/like/', ArticleLikesAPIView.as_view(), name='article-like'), # {'likes': 'likes'}는 ArticleRetrieveAPIView의 likes 메서드를 호출

    # Comments
    path('articles/<int:article_pk>/comments/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('articles/<int:article_pk>/comments/<int:pk>/', CommentRetrieveAPIView.as_view(), name='comment-retrieve'),
]
