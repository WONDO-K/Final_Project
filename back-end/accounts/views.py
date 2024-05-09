from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.views import APIView 

# Create your views here.
# 수정: class SearchView(View) -> class SearchView(APIView)
class SearchView(APIView):
    def get(self, request, task_id):
        return JsonResponse({'task_id': task_id}, status=200)