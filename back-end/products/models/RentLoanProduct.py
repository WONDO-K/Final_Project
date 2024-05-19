from django.db import models
from .bank import Bank

# 전세대출 상품 ---------------------------------------------------------------------
class RentLoanProduct(models.Model):
    dcls_month = models.CharField(max_length=6, verbose_name='공시 제출월 [YYYYMM]')
    fin_co_no = models.ForeignKey(Bank, on_delete=models.CASCADE)
    fin_prdt_cd = models.CharField(max_length=20, verbose_name='금융상품 코드')
    kor_co_nm = models.CharField(max_length=100, verbose_name='금융회사 명')
    fin_prdt_nm = models.CharField(max_length=100, verbose_name='금융 상품명')
    join_way = models.CharField(max_length=200, verbose_name='가입 방법')
    loan_inci_expn = models.TextField(verbose_name='대출 부대비용')
    erly_rpay_fee = models.CharField(max_length=200, verbose_name='조기 상환 수수료')
    dly_rate = models.TextField(verbose_name='연체 이자율')
    loan_lmt = models.CharField(max_length=200, verbose_name='대출 한도')
    dcls_strt_day = models.CharField(max_length=10, verbose_name='공시 시작일 [YYYY-MM-DD]')
    dcls_end_day = models.CharField(max_length=10, null=True, blank=True, verbose_name='공시 종료일 [YYYY-MM-DD]')
    fin_co_subm_day = models.CharField(max_length=20, verbose_name='금융회사 제출일 [YYYYMMDDHH24MI]')

    def __str__(self):
        return f'{self.fin_prdt_nm} ({self.fin_co_no})'

class RentLoanProductOption(models.Model):
    rent_loan_product = models.ForeignKey(RentLoanProduct, related_name='rent_loan_options', on_delete=models.CASCADE)
    dcls_month = models.CharField(max_length=6, verbose_name='공시 제출월 [YYYYMM]')
    fin_co_no = models.CharField(max_length=20, verbose_name='금융회사 코드')
    fin_prdt_cd = models.CharField(max_length=20, verbose_name='금융상품 코드')
    rpay_type = models.CharField(max_length=20, verbose_name='상환방식')
    rpay_type_nm = models.CharField(max_length=100, verbose_name='상환방식명')
    lend_rate_type = models.CharField(max_length=20, verbose_name='금리유형')
    lend_rate_type_nm = models.CharField(max_length=100, verbose_name='금리유형명')
    lend_rate_min = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='최소 금리')
    lend_rate_max = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='최대 금리')
    lend_rate_avg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='평균 금리')

    class Meta:
        verbose_name = '전세대출 상품 옵션'
        verbose_name_plural = '전세대출 상품 옵션 목록'

    def __str__(self):
        return f'{self.rent_loan.fin_prdt_nm} - {self.rpay_type_nm}'