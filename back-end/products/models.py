from django.db import models

class Bank(models.Model): # 은행
    fin_co_no = models.CharField(max_length=20, unique=True) # 금융회사 코드
    kor_co_nm = models.CharField(max_length=100) # 금융회사명
    homp_url = models.URLField() # 홈페이지 주소
    cal_tel = models.CharField(max_length=20)   

    def __str__(self): 
        return self.kor_co_nm 

class BankOption(models.Model): # 은행 옵션
    bank = models.ForeignKey(Bank, related_name='options', on_delete=models.CASCADE) # 은행
    area_cd = models.CharField(max_length=2) # 지역 코드   
    area_nm = models.CharField(max_length=50) # 지역명
    exis_yn = models.CharField(max_length=1) # 존재 여부

    def __str__(self):
        return f"{self.area_nm} - {self.fin_co_no}"

class DepositProduct(models.Model): # 정기 예금 상품
    fin_prdt_cd = models.CharField(max_length=20, unique=True)  # 금융상품 코드
    fin_co_no = models.ForeignKey(Bank, on_delete=models.CASCADE)  # 금융회사 코드
    kor_co_nm = models.CharField(max_length=100)  # 금융회사명
    fin_prdt_nm = models.CharField(max_length=100)  # 금융 상품명
    join_way = models.CharField(max_length=200)  # 가입 방법
    mtrt_int = models.TextField()  # 만기 후 이자율
    spcl_cnd = models.TextField()  # 우대조건
    join_deny = models.CharField(max_length=20)  # 가입제한
    join_member = models.CharField(max_length=100)  # 가입대상
    etc_note = models.TextField()  # 기타 유의사항
    max_limit = models.IntegerField(null=True, blank=True)  # 최고한도
    dcls_strt_day = models.CharField(max_length=10)  # 공시 시작일[YYYY-MM-DD]
    dcls_end_day = models.CharField(max_length=10,null=True, blank=True)  # 공시 종료일
    dcls_month = models.CharField(max_length=6)  # 공시 제출월 [YYYYMM]
    fin_co_subm_day = models.CharField(max_length=20)  # 금융회사 제출일 [YYYYMMDDHH24MI]

    def __str__(self):
        return self.fin_prdt_nm     
    
class DepositProductOption(models.Model): # 정기 예금 상품 옵션
    deposit_product = models.ForeignKey(DepositProduct, related_name='deposit_options', on_delete=models.CASCADE) # 정기 예금 상품, DepositProduct 실제 객체를 참조
    intr_rate_type = models.CharField(max_length=20) # 이자율 종류   
    intr_rate_type_nm = models.CharField(max_length=100) # 이자율 종류명
    save_trm = models.IntegerField() # 저축 기간
    intr_rate = models.DecimalField(max_digits=5, decimal_places=2) # 이자율
    intr_rate2 = models.DecimalField(max_digits=5, decimal_places=2) # 이자율2

    def __str__(self):
        return f"{self.deposit_product .fin_prdt_nm} - {self.intr_rate_type_nm}"


class SavingProduct(models.Model): # 적금 상품
    fin_prdt_cd = models.CharField(max_length=20, unique=True)  # 금융상품 코드
    fin_co_no = models.ForeignKey(Bank, on_delete=models.CASCADE)  # 금융회사 코드
    kor_co_nm = models.CharField(max_length=100)  # 금융회사명
    fin_prdt_nm = models.CharField(max_length=100)  # 금융 상품명
    join_way = models.CharField(max_length=200)  # 가입 방법
    mtrt_int = models.TextField()  # 만기 후 이자율
    spcl_cnd = models.TextField()  # 우대조건
    join_deny = models.CharField(max_length=20)  # 가입제한
    join_member = models.CharField(max_length=100)  # 가입대상
    etc_note = models.TextField()  # 기타 유의사항
    max_limit = models.IntegerField(null=True, blank=True)  # 최고한도
    dcls_strt_day = models.CharField(max_length=10)  # 공시 시작일[YYYY-MM-DD]
    dcls_end_day = models.CharField(max_length=10,null=True, blank=True)  # 공시 종료일
    dcls_month = models.CharField(max_length=6)  # 공시 제출월 [YYYYMM]
    fin_co_subm_day = models.CharField(max_length=20)  # 금융회사 제출일 [YYYYMMDDHH24MI]

    def __str__(self):
        return self.fin_prdt_nm
    
class SavingProductOption(models.Model): # 적금 상품 옵션
    saving_product = models.ForeignKey(SavingProduct, related_name='saving_options', on_delete=models.CASCADE) # 적금 상품, SavingProduct 실제 객체를 참조
    intr_rate_type = models.CharField(max_length=100, verbose_name='저축 금리 유형')
    intr_rate_type_nm = models.CharField(max_length=100, verbose_name='저축 금리 유형명')
    rsrv_type = models.CharField(max_length=100, verbose_name='적립 유형')
    rsrv_type_nm = models.CharField(max_length=100, verbose_name='적립 유형명')
    save_trm = models.IntegerField(verbose_name='저축 기간', help_text='단위: 개월')
    intr_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='저축 금리')
    intr_rate2 = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='최고 우대금리')

    class Meta:
        verbose_name = '저축 상품 옵션'
        verbose_name_plural = '저축 상품 옵션 목록'

    def __str__(self):
        return f'{self.intr_rate_type_nm} - {self.rsrv_type_nm}'

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