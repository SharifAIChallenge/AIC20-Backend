from django.db import models


# Create your models here.

class Staff(models.Model):
    title = models.CharField(max_length=256)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    image = models.FileField()
