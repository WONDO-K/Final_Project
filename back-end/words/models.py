from django.db import models

# Create your models here.
class Word(models.Model):
    economic_word = models.CharField(max_length=200)
    content = models.TextField()  # 설명을 저장하는 필드

    def __str__(self):
        return self.word