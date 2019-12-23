import markdown
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models


# Create your models here.
from rest_framework.validators import UniqueValidator


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True)
    text = models.TextField(max_length=200, null=False)
    seen = models.BooleanField(default=False, null=False)


class Subscriber(models.Model):
    email = models.EmailField(null=False, unique=True)


class EmailText(models.Model):
    text = models.TextField(null=False)
    html = models.TextField(editable=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.html = markdown.markdown(self.text)
