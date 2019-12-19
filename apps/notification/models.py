from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Notification(models.Model):
    user = models.OneToOneField(User, on_delet=models.CASCADE)
    title = models.CharField(max_lenght=50, null=True)
    text = models.TextField(null=False)
    seen = models.BooleanField(default=False)
