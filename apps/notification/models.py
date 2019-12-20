from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True)
    text = models.TextField(max_length=200, null=False)
    seen = models.BooleanField(default=False, null=False)


class Subscriber(models.Model):
    email = models.EmailField(null=False)


class EmailText(models.Model):
    text = models.TextField(max_length=500, null=False)
