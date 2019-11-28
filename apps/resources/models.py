from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=100)


class Section(models.Model):
    document = models.ForeignKey(Document, related_name='sections', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    md = models.FileField()


class Subtitle(models.Model):
    subtitle = models.CharField(max_length=50)
    section = models.ForeignKey(Section, related_name='subtitles', on_delete=models.CASCADE)
