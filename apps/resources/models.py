import uuid

from django.db import models


class Document(models.Model):
    title_en = models.CharField(max_length=100, unique=True)
    title_fa = models.CharField(
        max_length=100, unique=True, blank=True, null=False)
    description_en = models.TextField(blank=True, null=False)
    description_fa = models.TextField(blank=True, null=False)

    thumbnail = models.ImageField(upload_to='document/thumbnails/', null=True)
    file = models.FileField(upload_to='document/files/', null=True)

    order = models.PositiveSmallIntegerField(default=0)

    time_to_read = models.PositiveSmallIntegerField(default=10)

    def __str__(self):
        return self.title_en


class Section(models.Model):
    document = models.ForeignKey(
        Document, related_name='sections', on_delete=models.CASCADE, null=True)
    title_en = models.CharField(max_length=100)
    title_fa = models.CharField(max_length=100, blank=True, null=False)
    markdown = models.TextField(blank=True)
    uuid = models.CharField(max_length=20, unique=True, blank=True, null=False)

    order = models.PositiveSmallIntegerField(default=0)

    @staticmethod
    def generate_uuid():
        return uuid.uuid4().hex[:16]

    def pre_save(self):
        self.uuid = Section.generate_uuid()

    def save(self, *args, **kwargs):
        self.pre_save()
        super(Section, self).save(*args, **kwargs)

    def __str__(self):
        return self.title_en


class Subsection(models.Model):
    subtitle_en = models.CharField(max_length=50)
    subtitle_fa = models.CharField(max_length=50, blank=True, null=False)
    section = models.ForeignKey(
        Section, related_name='subtitles', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.subtitle_en
