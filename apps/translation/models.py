from django.db import models

class TranslatedText(models.Model):
    content_en = models.TextField(blank=True, null=False)
    content_fa = models.TextField(blank=True, null=False)

    def __str__(self):
        return self.content_en