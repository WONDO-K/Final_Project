import requests, os
from django.http import JsonResponse
from rest_framework.views import APIView
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny

NAVER_CLIENT_ID = os.environ['NAVER_CLIENT_ID']
NAVER_CLIENT_SECRET = os.environ['NAVER_CLIENT_SECRET']


class NewsSearchAPIView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_summary='뉴스 정보를 가져옵니다.',
        tags=['뉴스'],
        responses={
            200: 'Success',
            500: 'Failed to fetch data from Naver API'
        }
    )
    def get(self, request):
        query = '경제'

        url = 'https://openapi.naver.com/v1/search/news.json'
        headers = {
            'X-Naver-Client-Id': settings.NAVER_CLIENT_ID,
            'X-Naver-Client-Secret': settings.NAVER_CLIENT_SECRET,
        }
        params = {
            'query': query,
            'display': 10,
            'start': 1,
            'sort': 'sim'
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            results = [{'title': item['title'], 'originallink': item['originallink']} for item in items]
            return JsonResponse({'results': results})
        else:
            return JsonResponse({'error': 'Failed to fetch data from Naver API'}, status=response.status_code)

