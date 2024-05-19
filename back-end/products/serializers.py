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
from .models import UserDepositProduct, UserSavingProduct, UserPensionProduct, UserRentLoanProduct

class JoinProductSerializer(serializers.Serializer): # 사용자가 상품에 가입할 때 사용하는 시리얼라이저
    product_type = serializers.CharField(max_length=20) # 'deposit', 'saving', 'pension', 'rent_loan' 중 하나로 상품 타입을 의미
    product_id = serializers.IntegerField() # 상품 ID
    option_id = serializers.IntegerField() # 상품 옵션 ID


class UserProductSerializer(serializers.ModelSerializer):
    class Meta: # UserProductSerializer를 상속받는 Serializer 클래스에서 Meta 클래스를 정의할 때 상속받는 클래스의 Meta 클래스를 참조하도록 함
        fields = ['user', 'product_type', 'selected_option', 'join_date']

class UserDepositProductSerializer(UserProductSerializer):
    class Meta(UserProductSerializer.Meta): 
        model = UserDepositProduct
        fields = UserProductSerializer.Meta.fields + ['deposit_product'] # UserProductSerializer의 fields에 'deposit_product' 필드를 추가

class UserSavingProductSerializer(UserProductSerializer):
    class Meta(UserProductSerializer.Meta):
        model = UserSavingProduct
        fields = UserProductSerializer.Meta.fields + ['saving_product']

class UserPensionProductSerializer(UserProductSerializer):
    class Meta(UserProductSerializer.Meta):
        model = UserPensionProduct
        fields = UserProductSerializer.Meta.fields + ['pension_product']

class UserRentLoanProductSerializer(UserProductSerializer):
    class Meta(UserProductSerializer.Meta):
        model = UserRentLoanProduct
        fields = UserProductSerializer.Meta.fields + ['rent_loan_product']

# class UserProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = ['id', 'user', 'selected_option', 'join_date']

# class DynamicUserProductSerializer(serializers.ModelSerializer):
#     class Meta(UserProductSerializer.Meta):
#         pass
    
#     def __init__(self, *args, **kwargs):
#         model = kwargs.pop('model', None)
#         super().__init__(*args, **kwargs)
#         if model:
#             self.Meta.model = model # 상품 모델을 동적으로 변경
#             self.Meta.fields += [model.product_field] # 상품 필드명을 동적으로 추가