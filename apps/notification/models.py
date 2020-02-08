import markdown
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models

# Create your models here.
from rest_framework.validators import UniqueValidator


class Notification(models.Model):
    users = models.ManyToManyField(User, related_name='notifications')
    title = models.CharField(max_length=50, null=True)
    text = models.TextField(max_length=200, null=False)
    seen = models.BooleanField(default=False, null=False)
    for_all = models.BooleanField(default=False)

    def pre_save(self):
        if self.for_all:
            self.users = list(User.objects.all())

    def save(self, *args, **kwargs):
        self.pre_save()
        super().save(*args, **kwargs)


class Subscriber(models.Model):
    email = models.EmailField(null=False, unique=True)


class EmailText(models.Model):
    text = models.TextField(null=False)
    html = models.TextField(editable=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.html = markdown.markdown(self.text)
