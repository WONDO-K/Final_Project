from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Word
from bs4 import BeautifulSoup
import requests
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
import os

API_KEY = os.environ['ECONOMINC_API_KEY']
class WordProcessingAPIView(APIView):

    @swagger_auto_schema(operation_summary="경제 사전을 생성합니다.", 
                        tags=['경제용어사전'],
                        responses={200: '단어 리스트 조회 성공'})
    def get(self, request, *args, **kwargs):
        try:
            # 웹 크롤링 시작
            for page_num in range(1, 11):  
                url = f"https://khiss.go.kr/board?pageNum={page_num}&rowCnt=10&menuId=MENU00317&schType=0&schText=&boardStyle=&categoryId=&continent=&schStartChar=&schEndChar=&country=&upDown=0"
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                dt_tags = soup.find_all('dt')
                for dt in dt_tags:
                    word = dt.text.split('(')[0].strip()
                    # 이미 존재하는 단어인지 확인 후 저장
                    if not Word.objects.filter(economic_word=word).exists():
                        Word.objects.create(economic_word=word)

            # API 호출 및 데이터 저장
            for word in Word.objects.all():
                url = f"http://ecos.bok.or.kr/api/StatisticWord/{API_KEY}/json/kr/1/1/{word.economic_word}"
                response = requests.get(url)
                if response.status_code == 200:
                    api_data = response.json()
                    row = api_data.get('StatisticWord', {}).get('row', [])
                    if row:
                        content = row[0].get('CONTENT')
                        if content:
                            word.content = content
                            word.save()

            # content가 비어있는 단어 삭제
            Word.objects.filter(content='').delete()

            return Response({"message": "작업이 완료되었습니다."}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class randomWordAPIView(APIView):
    @swagger_auto_schema(operation_summary="랜덤 단어를 조회합니다.", 
                        tags=['경제용어사전'],
                        responses={200: '랜덤 단어 조회 성공'})
    def get(self, request, *args, **kwargs):
        try:
            word = Word.objects.order_by('?').first()
            return JsonResponse({"word": word.economic_word, "content": word.content})
        except Exception as e:
            return Response({"error": str(e)}, status=500)