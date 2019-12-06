from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    EDUCATION_CHOICES = (
        ('high_school', 'دبیرستان'),
        ('bachelor', 'کارشناسی'),
        ('master', 'کارشناسی ارشد'),
        ('phd', 'دکنری')
    )
    email = models.EmailField()
    first_name_fa = models.TextField(max_length=100)
    first_name_en = models.TextField(max_length=100)
    last_name_fa = models.TextField(max_length=100)
    last_name_en = models.TextField(max_length=100)
    birth_date = models.DateTimeField()
    residence = models.CharField(max_length=100)
    education = models.CharField(
        max_length=15,
        choices=EDUCATION_CHOICES,
    )
