from rest_framework import serializers
from .models import *

class BankOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankOption
        fields = ['area_cd', 'area_nm', 'exis_yn']

class BankSerializer(serializers.ModelSerializer):
    options = BankOptionSerializer(many=True)  # BankOptionSerializer 포함
    
    class Meta:
        model = Bank
        fields = ['fin_co_no', 'kor_co_nm', 'homp_url', 'cal_tel', 'options']

class DepositProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProduct
        fields = '__all__'