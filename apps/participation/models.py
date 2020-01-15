from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Badge(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    image = models.ImageField()
    challenge = models.ForeignKey('challenge.Challenge', related_name='badges', on_delete=models.CASCADE)


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    badges = models.ManyToManyField('participation.Badge', related_name='teams')
    challenge = models.ForeignKey('challenge.Challenge', related_name='teams', on_delete=models.CASCADE)


class Participant(models.Model):
    user = models.OneToOneField(User, related_name='participant', on_delete=models.CASCADE)
    teams = models.ManyToManyField('participation.Team', related_name='participants')
