from django.db import models
from django.core.exceptions import ValidationError


class Redirect(models.Model):
    source = models.CharField(max_length=512, unique=True)
    destination = models.CharField(max_length=512)
    hits = models.IntegerField(default=0)

    def __str__(self):
        return '%s %s' % (self.source, self.destination)

    def clean(self):
        if not (self.destination.startswith("http") or self.destination.startswith("https")):
            raise ValidationError('URL should start with "http" or "https"')

