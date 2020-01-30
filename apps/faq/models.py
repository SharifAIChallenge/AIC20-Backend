from django.db import models


# Create your models here.


class Question(models.Model):
    title = models.CharField(max_length=128, blank=True, null=False)
    body = models.CharField(max_length=1024)


class Answer(models.Model):
    title = models.CharField(max_length=128, blank=True, null=False)
    body = models.CharField(max_length=1024)
    question = models.OneToOneField('faq.Question', related_name='answer', on_delete=models.CASCADE)
