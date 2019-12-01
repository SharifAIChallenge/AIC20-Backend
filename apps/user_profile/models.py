from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Profile(AbstractUser):
    email = models.EmailField()
    first_name = models.TextField(max_length=100)
