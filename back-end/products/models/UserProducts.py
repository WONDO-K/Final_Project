from django.db import models
from django.conf import settings
from .SavingProduct import SavingProduct, SavingProductOption
from .DepositProduct import DepositProduct, DepositProductOption
from .PensionProduct import PensionProduct, PensionProductOption
from .RentLoanProduct import RentLoanProduct, RentLoanProductOption

class UserDepositProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='deposit_products') # related_name: 역참조 시 사용할 이름
    product_type = models.CharField(max_length=10)  # 상품 타입
    deposit_product = models.ForeignKey(DepositProduct, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(DepositProductOption, on_delete=models.CASCADE) # 선택한 상품 옵션
    join_date = models.DateField()  # 가입 일자

    class Meta:
        unique_together = ('user', 'deposit_product')

class UserSavingProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saving_products')
    product_type = models.CharField(max_length=10)  # 상품 타입
    saving_product = models.ForeignKey(SavingProduct, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(SavingProductOption, on_delete=models.CASCADE)
    join_date = models.DateField()  # 가입 일자

    class Meta:
        unique_together = ('user', 'saving_product')

class UserPensionProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pension_products')
    product_type = models.CharField(max_length=10)  # 상품 타입
    pension_product = models.ForeignKey(PensionProduct, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(PensionProductOption, on_delete=models.CASCADE)
    join_date = models.DateField()  # 가입 일자

    class Meta:
        unique_together = ('user', 'pension_product')

class UserRentLoanProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rent_loan_products')
    product_type = models.CharField(max_length=10)  # 상품 타입
    rent_loan_product = models.ForeignKey(RentLoanProduct, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(RentLoanProductOption, on_delete=models.CASCADE)
    join_date = models.DateField()  # 가입 일자

    class Meta:
        unique_together = ('user', 'rent_loan_product')
