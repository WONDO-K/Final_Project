from django.db import models

# 연금 상품 ---------------------------------------------------------------------
class PensionProduct(models.Model):
    dcls_month = models.CharField(max_length=6)  # 공시 제출월 [YYYYMM]
    fin_co_no = models.CharField(max_length=20)  # 금융회사 코드
    kor_co_nm = models.CharField(max_length=100)  # 금융회사 명
    fin_prdt_cd = models.CharField(max_length=20)  # 금융상품 코드
    fin_prdt_nm = models.CharField(max_length=100)  # 금융 상품명
    join_way = models.CharField(max_length=200)  # 가입 방법
    pnsn_kind = models.CharField(max_length=20)  # 연금종류
    pnsn_kind_nm = models.CharField(max_length=100)  # 연금종류명
    sale_strt_day = models.CharField(max_length=10,null=True, blank=True)  # 판매 개시일 [YYYY-MM-DD]
    mntn_cnt = models.IntegerField()  # 유지건수[단위: 건] 또는 설정액 [단위: 원]
    prdt_type = models.CharField(max_length=20)  # 상품유형
    prdt_type_nm = models.CharField(max_length=100)  # 상품유형명
    dcls_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # 공시이율 [소수점 2자리]
    guar_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # 최저 보증이율
    btrm_prft_rate_1 = models.DecimalField(max_digits=5, decimal_places=2)  # 과거 수익률1(전년도) [소수점 2자리]
    btrm_prft_rate_2 = models.DecimalField(max_digits=5, decimal_places=2)  # 과거 수익률2(전전년도) [소수점 2자리]
    btrm_prft_rate_3 = models.DecimalField(max_digits=5, decimal_places=2)  # 과거 수익률3(전전전년도) [소수점 2자리]
    etc = models.TextField(null=True, blank=True)  # 기타사항
    sale_co = models.CharField(max_length=100)  # 판매사
    dcls_strt_day = models.CharField(max_length=10)  # 공시 시작일 [YYYY-MM-DD]
    dcls_end_day = models.CharField(max_length=10,null=True, blank=True)  # 공시 종료일 [YYYY-MM-DD]
    fin_co_subm_day = models.CharField(max_length=20)  # 금융회사 제출일 [YYYYMMDDHH24MI]

    def __str__(self):
        return f'{self.fin_prdt_nm} ({self.fin_co_no})'


class PensionProductOption(models.Model):
    pension_product = models.ForeignKey(PensionProduct, related_name='pension_options', on_delete=models.CASCADE)
    dcls_month = models.CharField(max_length=6, verbose_name='공시 제출월 [YYYYMM]')
    fin_co_no = models.CharField(max_length=20, verbose_name='금융회사 코드')
    fin_prdt_cd = models.CharField(max_length=20, verbose_name='금융상품 코드')
    pnsn_recp_trm = models.CharField(max_length=20, verbose_name='연금수령기간')
    pnsn_recp_trm_nm = models.CharField(max_length=100, verbose_name='연금수령기간명')
    pnsn_entr_age = models.CharField(max_length=20, verbose_name='연금가입나이')
    pnsn_entr_age_nm = models.CharField(max_length=100, verbose_name='연금가입나이명')
    mon_paym_atm = models.CharField(max_length=20, verbose_name='월납입금액')
    mon_paym_atm_nm = models.CharField(max_length=100, verbose_name='월납입금액명')
    paym_prd = models.CharField(max_length=20, verbose_name='납입기간')
    paym_prd_nm = models.CharField(max_length=100, verbose_name='납입기간명')
    pnsn_strt_age = models.CharField(max_length=20, verbose_name='연금개시나이')
    pnsn_strt_age_nm = models.CharField(max_length=100, verbose_name='연금개시나이명')
    pnsn_recp_amt = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='연금수령금액')

    class Meta:
        verbose_name = '연금 상품 옵션'
        verbose_name_plural = '연금 상품 옵션 목록'

    def __str__(self): # 연금 상품 옵션명
        return f'{self.pension_product.fin_prdt_nm} - {self.pnsn_recp_trm_nm}' # 연금 상품명 - 연금수령기간명
