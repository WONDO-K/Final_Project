from django.db import models

class Bank(models.Model):
    fin_co_no = models.CharField(max_length=20, unique=True)
    kor_co_nm = models.CharField(max_length=100)
    homp_url = models.URLField()
    cal_tel = models.CharField(max_length=20)

    def __str__(self):
        return self.kor_co_nm

class Option(models.Model):
    bank = models.ForeignKey(Bank, related_name='options', on_delete=models.CASCADE)
    area_cd = models.CharField(max_length=2)
    area_nm = models.CharField(max_length=50)
    exis_yn = models.CharField(max_length=1)

    def __str__(self):
        return f"{self.area_nm} - {self.fin_co_no}"