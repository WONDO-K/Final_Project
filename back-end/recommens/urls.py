from django.urls import path
from .views import TopProductsView,SimmilarRecommendProductsAPIView

app_name = 'recommens'

urlpatterns = [
    # 가입자 수가 많은 상품 5개를 가져오는 API
    path('top-products/', TopProductsView.as_view(), name='top-products'),

    # 비슷한 사용자 정보를 가진 사람들의 가입 상품을 추천하는 API
    path('similar-products/', SimmilarRecommendProductsAPIView.as_view(), name='similar-products'),
]