from rest_framework import serializers
from .models import Bank, Option

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['area_cd', 'area_nm', 'exis_yn']

class BankSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)  # OptionSerializer를 포함
    
    class Meta:
        model = Bank
        fields = ['fin_co_no', 'kor_co_nm', 'homp_url', 'cal_tel', 'options']
