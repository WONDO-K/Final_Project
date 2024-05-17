from rest_framework import serializers
from .models import *

class BankOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankOption 
        fields = ['area_cd', 'area_nm', 'exis_yn']

class BankSerializer(serializers.ModelSerializer):
    options = BankOptionSerializer(many=True)  # BankOptionSerializer 포함(역참조, 여러 개의 BankOption 객체를 시리얼라이즈)
    
    class Meta:
        model = Bank
        fields = ['fin_co_no', 'kor_co_nm', 'homp_url', 'cal_tel', 'options']

class DepositProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProductOption
        fields = ['intr_rate_type', 'intr_rate_type_nm', 'save_trm', 'intr_rate', 'intr_rate2']

class DepositProductSerializer(serializers.ModelSerializer): 

    # related_name='deposit_options'로 지정한 필드명을 사용
    deposit_options = DepositProductOptionSerializer(many=True)  # DepositProductOptionSerializer 포함(역참조, 여러 개의 DepositProductOption 객체를 시리얼라이즈)

    class Meta:
        model = DepositProduct
        fields = ['fin_prdt_cd', 'fin_co_no', 'fin_prdt_nm', 'join_way', 'mtrt_int', 'spcl_cnd', 'join_deny', 'join_member', 'etc_note', 'max_limit', 'dcls_strt_day', 'dcls_end_day', 'dcls_month', 'fin_co_subm_day', 'deposit_options']