from django.db import models

class Bank(models.Model):
    fin_co_no = models.CharField(max_length=20, unique=True)
    kor_co_nm = models.CharField(max_length=100)
    homp_url = models.URLField()
    cal_tel = models.CharField(max_length=20)

    def __str__(self):
        return self.kor_co_nm

class BankOption(models.Model):
    bank = models.ForeignKey(Bank, related_name='options', on_delete=models.CASCADE)
    area_cd = models.CharField(max_length=2)
    area_nm = models.CharField(max_length=50)
    exis_yn = models.CharField(max_length=1)

    def __str__(self):
        return f"{self.area_nm} - {self.fin_co_no}"
    
class DepositProductOption(models.Model):
    deposit_product = models.ForeignKey('DepositProduct', on_delete=models.CASCADE)
    intr_rate_type = models.CharField(max_length=20)
    intr_rate_type_nm = models.CharField(max_length=100)
    save_trm = models.IntegerField()
    intr_rate = models.DecimalField(max_digits=5, decimal_places=2)
    intr_rate2 = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.deposit_product .fin_prdt_nm} - {self.intr_rate_type_nm}"

class DepositProduct(models.Model):
    fin_prdt_cd = models.CharField(max_length=20, unique=True)  # 금융상품 코드
    fin_co_no = models.ForeignKey(Bank, on_delete=models.CASCADE)  # 금융회사 코드
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