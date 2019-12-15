from django.db import models


class TranslatedText(models.Model):
    content_en = models.TextField(blank=True, null=False)
    content_fa = models.TextField(blank=True, null=False)

    def __str__(self):
        return self.content_en


def translatedTextField(related_name):
    return models.ForeignKey(
        TranslatedText,
        models.CASCADE,
        related_name=related_name
    )


class DocumentTest(models.Model):
    title = translatedTextField(related_name='title')
    description = translatedTextField(related_name='description')

    def __str__(self):
        return str(self.title)
