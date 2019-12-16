import uuid

from django.db import models

from apps.translation.models import translatedTextField


class Document(models.Model):
    title = translatedTextField(related_name='title')
    description = translatedTextField(related_name='description')

    def __str__(self):
        return self.title.content_en


class Section(models.Model):
    document = models.ForeignKey(
        Document, related_name='sections', on_delete=models.CASCADE, null=True)
    title = translatedTextField(related_name='title')
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
        return self.title.content_en


class Subsection(models.Model):
    subtitle = translatedTextField(related_name='subtitle')
    section = models.ForeignKey(
        Section, related_name='subtitles', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.subtitle.content_en
