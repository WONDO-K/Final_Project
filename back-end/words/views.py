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

class WebCrowlerAPIView(APIView):

    @swagger_auto_schema(
            operation_summary="크롤링을 통해 단어 저장하기",
            tags=['경제 용어 사전'],)
    def get(self, request, *args, **kwargs):
        for page_num in range(1, 11):  
            url = f"https://khiss.go.kr/board?pageNum={page_num}&rowCnt=10&menuId=MENU00317&schType=0&schText=&boardStyle=&categoryId=&continent=&schStartChar=&schEndChar=&country=&upDown=0"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            dt_tags = soup.find_all('dt')
            for dt in dt_tags:
                word = dt.text.split('(')[0].strip()
                Word.objects.create(economic_word=word)

        # 단어 저장 후 응답
        return Response({"message": "데이터가 성공적으로 크롤링되어 저장되었습니다."}, status=201)

class DictionaryAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="경제 용어 API 호출하기",
        tags=['경제 용어 사전']
    )
    def get(self, request, *args, **kwargs):
        words = Word.objects.all()
        for word in words:
            url = f"http://ecos.bok.or.kr/api/StatisticWord/{API_KEY}/json/kr/1/1/{word.economic_word}"
            response = requests.get(url)
            if response.status_code == 200:
                api_data = response.json()
                if 'StatisticWord' in api_data:
                    row = api_data['StatisticWord'].get('row', [])
                    if row:
                        item = row[0]
                        content = item.get('CONTENT', None)
                        word.content = content
                        word.save()
        return JsonResponse(data={"message": "API 호출 및 데이터 저장 완료"}, status=201)
    

class CleanUpWordsAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="content가 없는 단어 삭제",
        tags=['경제 용어 사전']
    )
    def post(self, request, *args, **kwargs):
        try:
            # content가 비어있는 단어 객체들을 가져옵니다.
            words_without_content = Word.objects.filter(content__exact='')

            # 가져온 단어 객체들을 삭제합니다.
            words_without_content.delete()

            return JsonResponse(data={"message": "content가 없는 단어 삭제 완료"}, status=200)
        except Exception as e:
            # 실패 시 처리
            return JsonResponse(data={"message": "content가 없는 단어 삭제 실패", "error": str(e)}, status=400)
        

class WordListAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="경제 용어 리스트 반환",
        tags=['경제 용어 사전']
    )
    def get(self, request, *args, **kwargs):
        words = Word.objects.all()
        data = []
        for word in words:
            data.append({
                "economic_word": word.economic_word,
                "content": word.content
            })
        return JsonResponse(data={"data": data}, status=200)

class WordDetailAPIView(APIView):
    
        @swagger_auto_schema(
            operation_summary="경제 용어 상세 정보 반환",
            tags=['경제 용어 사전']
        )
        def get(self, request, pk, *args, **kwargs):
            try:
                word = Word.objects.get(pk=pk)
                data = {
                    "economic_word": word.economic_word,
                    "content": word.content
                }
                return JsonResponse(data={"data": data}, status=200)
            except Word.DoesNotExist:
                return JsonResponse(data={"message": "해당하는 단어가 없습니다."}, status=404)
            except Exception as e:
                return JsonResponse(data={"message": "서버 에러", "error": str(e)}, status=500)