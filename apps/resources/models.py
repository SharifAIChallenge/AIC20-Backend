from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=100, unique=True, primary_key=True)

    def __str__(self):
        return self.title


class Section(models.Model):
    document = models.ForeignKey(Document, related_name='sections', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    markdown = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Subtitle(models.Model):
    subtitle = models.CharField(max_length=50)
    section = models.ForeignKey(Section, related_name='subtitles', on_delete=models.CASCADE)

    def __str__(self):
        return self.subtitle
