from django.db import models

# Create your models here.
class CurrencyRate(models.Model):
    
    cur_nm = models.CharField(max_length=50,default='') # 통화명
    cur_unit = models.CharField(max_length=50) # 통화단위
    deal_bas_r = models.CharField(max_length=20) # 매매기준율

    def __str__(self): # 객체를 출력할 때 나타날 문자열을 지정
        return self.cur_unit