from django.contrib.auth.models import AbstractUser, User
from django.db import models

# Create your models here.


class Profile(AbstractUser):
    high_school = 'HS'
    bachelor = ' BR'
    master = 'MR'
    phd = 'PHD'

    EDUCATION_CHOICES = (
        (high_school, 'دبیرستان'),
        (bachelor, 'کارشناسی'),
        (master, 'کارشناسی ارشد'),
        (phd, 'دکنری')
    )
    email = models.EmailField()
    first_name_fa = models.TextField(max_length=100, null=True)
    first_name_en = models.TextField(max_length=100, null=True)
    last_name_fa = models.TextField(max_length=100, null=True)
    last_name_en = models.TextField(max_length=100, null=True)
    birth_date = models.DateTimeField(null=True)
    residence = models.BooleanField(null=True)
    education = models.CharField(
        max_length=3,
        choices=EDUCATION_CHOICES,
        default=high_school
    )

