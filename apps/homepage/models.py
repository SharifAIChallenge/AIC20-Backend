from django.db import models


class Intro(models.Model):
    header_en = models.CharField(max_length=100)
    header_fa = models.CharField(max_length=100)
    text_en = models.TextField()
    text_fa = models.TextField()


class TimelineEvent(models.Model):
    date = models.DateTimeField()
    title_en = models.CharField(max_length=100)
    title_fa = models.CharField(max_length=100)
    text_en = models.TextField()
    text_fa = models.TextField()

    order = models.PositiveSmallIntegerField(default=1)


class Prize(models.Model):
    title_en = models.CharField(max_length=100)
    title_fa = models.CharField(max_length=100)
    prize_en = models.CharField(max_length=100)
    prize_fa = models.CharField(max_length=100)


class Stat(models.Model):
    title_en = models.CharField(max_length=100)
    title_fa = models.CharField(max_length=100)
    stat_en = models.CharField(max_length=100)
    stat_fa = models.CharField(max_length=100)

