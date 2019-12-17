from django.db import models


class Intro(models.Model):
    header = models.CharField(max_length=100)
    text = models.TextField()


class TimelineEvent(models.Model):
    date = models.DateTimeField()
    title = models.CharField(max_length=100)
    text = models.TextField()


class Prize(models.Model):
    title = models.CharField(max_length=20)
    prize = models.CharField(max_length=20)


class Stat(models.Model):
    title = models.CharField(max_length=20)
    stat = models.CharField(max_length=20)

