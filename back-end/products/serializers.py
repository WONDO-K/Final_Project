from rest_framework import serializers
from .models import Bank, BankOption, DepositProduct, DepositProductOption, SavingProduct, SavingProductOption, PensionProduct, PensionProductOption, RentLoanProduct, RentLoanProductOption


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
        fields = [
            'intr_rate_type', 'intr_rate_type_nm', 
            'save_trm', 'intr_rate', 'intr_rate2']

class DepositProductSerializer(serializers.ModelSerializer): 

    # related_name='deposit_options'로 지정한 필드명을 사용
    deposit_options = DepositProductOptionSerializer(many=True)  # DepositProductOptionSerializer 포함(역참조, 여러 개의 DepositProductOption 객체를 시리얼라이즈)

    class Meta:
        model = DepositProduct
        fields = [
            'fin_prdt_cd','kor_co_nm', 'fin_co_no', 'fin_prdt_nm', 
            'join_way', 'mtrt_int', 'spcl_cnd', 'join_deny', 'join_member', 
            'etc_note', 'max_limit', 'dcls_strt_day', 'dcls_end_day', 'dcls_month', 
            'fin_co_subm_day', 'deposit_options']
        
class SavingProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProductOption
        fields = [
            'intr_rate_type','intr_rate_type_nm','rsrv_type','rsrv_type_nm',
            'save_trm','intr_rate','intr_rate2']

class SavingProductSerializer(serializers.ModelSerializer):

    saving_options = SavingProductOptionSerializer(many=True)  # SavingProductOptionSerializer 포함(역참조, 여러 개의 SavingProductOption 객체를 시리얼라이즈)

    class Meta:
        model = SavingProduct
        fields = [
            'fin_prdt_cd', 'kor_co_nm', 'fin_co_no', 'fin_prdt_nm', 
            'join_way', 'mtrt_int', 'spcl_cnd', 'join_deny', 'join_member', 
            'etc_note', 'max_limit', 'dcls_strt_day', 'dcls_end_day', 'dcls_month', 
            'fin_co_subm_day','saving_options']

class PensionProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PensionProductOption
        fields = [
            'dcls_month', 'fin_co_no', 'fin_prdt_cd', 'pnsn_recp_trm',
            'pnsn_recp_trm_nm', 'pnsn_entr_age', 'pnsn_entr_age_nm',
            'mon_paym_atm', 'mon_paym_atm_nm', 'paym_prd', 'paym_prd_nm',
            'pnsn_strt_age', 'pnsn_strt_age_nm', 'pnsn_recp_amt'
        ]
        
class PensionProductSerializer(serializers.ModelSerializer):

    pension_options = PensionProductOptionSerializer(many=True, read_only=True)

    class Meta:
        model = PensionProduct
        fields = [
            'dcls_month', 'fin_co_no', 'kor_co_nm', 'fin_prdt_cd', 
            'fin_prdt_nm', 'join_way', 'pnsn_kind', 'pnsn_kind_nm', 
            'sale_strt_day', 'mntn_cnt', 'prdt_type', 'prdt_type_nm', 
            'dcls_rate', 'guar_rate', 'btrm_prft_rate_1', 'btrm_prft_rate_2', 
            'btrm_prft_rate_3', 'etc', 'sale_co', 'dcls_strt_day', 
            'dcls_end_day', 'fin_co_subm_day', 'pension_options'
        ]

class RentLoanOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentLoanProductOption
        fields = [
            'dcls_month', 'fin_co_no', 'fin_prdt_cd', 'rpay_type', 
            'rpay_type_nm', 'lend_rate_type', 'lend_rate_type_nm', 
            'lend_rate_min', 'lend_rate_max', 'lend_rate_avg'
        ]

class RentLoanSerializer(serializers.ModelSerializer):
    rent_loan_options = RentLoanOptionSerializer(many=True, read_only=True)  # RentLoanOptionSerializer 포함(역참조)

    class Meta:
        model = RentLoanProduct
        fields = [
            'dcls_month', 'fin_co_no', 'kor_co_nm', 'fin_prdt_cd', 
            'fin_prdt_nm', 'join_way', 'loan_inci_expn', 'erly_rpay_fee', 
            'dly_rate', 'loan_lmt', 'dcls_strt_day', 'dcls_end_day', 
            'fin_co_subm_day', 'rent_loan_options'
        ]