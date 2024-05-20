from django.db import models

class Bank(models.Model): # 은행
    dcls_month = models.CharField(max_length=6) # 공시 제출월 [YYYYMM]
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