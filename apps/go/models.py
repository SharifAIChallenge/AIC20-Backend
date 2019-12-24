from django.db import models


# Create your models here.
class Redirect(models.Model):
    source = models.CharField(max_length=50,unique=True)
    destination = models.CharField(max_length=50,unique=True)

