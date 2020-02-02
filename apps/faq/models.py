from django.db import models


# Create your models here.


class QuestionWithAnswer(models.Model):
    question_en = models.CharField(max_length=1024)
    question_fa = models.CharField(max_length=1024)
    answer_en = models.CharField(max_length=1024)
    answer_fa = models.CharField(max_length=1024)
