from django.contrib.auth.models import User
from django.db import models
from apps.translation.models import translatedTextField


class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='profile')

    EDUCATION_CHOICES = (
        ('high_school', 'دبیرستان'),
        ('bachelor', 'کارشناسی'),
        ('master', 'کارشناسی ارشد'),
        ('phd', 'دکنری')
    )
    email = models.EmailField()
    first_name = translatedTextField(related_name='first_name')
    last_name = translatedTextField(related_name='last_name')
    birth_date = models.DateField()
    residence = models.CharField(max_length=100)
    education = models.CharField(
        max_length=15,
        choices=EDUCATION_CHOICES,
    )
