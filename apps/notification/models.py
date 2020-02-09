import markdown
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models


# Create your models here.


class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=50, null=True)
    text = models.TextField(max_length=200, null=False)
    seen = models.BooleanField(default=False, null=False)
    create_date = models.DateTimeField(auto_now_add=True)
    for_all = models.BooleanField(default=False)

    def pre_save(self):
        if self.user is None:
            self.for_all = True

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
