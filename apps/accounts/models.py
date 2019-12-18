from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):

    EDUCATION_CHOICES = (
        ('high_school', 'دبیرستان'),
        ('bachelor', 'کارشناسی'),
        ('master', 'کارشناسی ارشد'),
        ('phd', 'دکنری')
    )

    user = models.OneToOneField(User,
        on_delete=models.CASCADE,
        related_name='profile')
    firstname_fa = models.TextField(max_length=30)
    firstname_en = models.TextField(max_length=30)
    lastname_fa = models.TextField(max_length=30)
    lastname_en = models.TextField(max_length=30)
    birth_date = models.DateField()
    university = models.CharField(max_length=50)
    education = models.CharField(
        max_length=15,
        choices=EDUCATION_CHOICES,
    )

