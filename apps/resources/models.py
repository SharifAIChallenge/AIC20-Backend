import uuid

from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=100, unique=True, primary_key=True)

    def __str__(self):
        return self.title


class Section(models.Model):
    document = models.ForeignKey(Document, related_name='sections', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    markdown = models.TextField(blank=True)
    uuid = models.CharField(max_length=20, unique=True, blank=True, null=False)

    @staticmethod
    def generate_uuid():
        return uuid.uuid4().hex[:16]

    def pre_save(self):
        self.uuid = Section.generate_uuid()

    def save(self, *args, **kwargs):
        self.pre_save()
        super(Section, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Subtitle(models.Model):
    subtitle = models.CharField(max_length=50)
    section = models.ForeignKey(Section, related_name='subtitles', on_delete=models.CASCADE)

    def __str__(self):
        return self.subtitle
