from django.db import models

# Create your models here.
class CurrencyRate(models.Model):
    
    cur_nm = models.CharField(max_length=50, default='')  # 통화명
    cur_unit = models.CharField(max_length=50)  # 통화단위
    ttb = models.DecimalField(max_digits=10, decimal_places=2)  # 전신환(송금) 보내실 때
    tts = models.DecimalField(max_digits=10, decimal_places=2)  # 전신환(송금) 받으실 때

    def __str__(self):
        return self.cur_unit

    def save(self, *args, **kwargs):
        # ttb와 tts 값을 문자열에서 실수로 변환하여 저장
        self.ttb = self.ttb.replace(',', '') if self.ttb else 0
        self.tts = self.tts.replace(',', '') if self.tts else 0
        super().save(*args, **kwargs)
