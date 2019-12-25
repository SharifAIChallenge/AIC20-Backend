from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

class Redirect(models.Model):
    source = models.CharField(max_length=50, unique=True)
    destination = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return '%s %s' % (self.source, self.destination)

    def clean(self):
        if not (self.destination.startswith("http") or self.destination.startswith("https")):
            raise ValidationError('URL should start with "http" or "https"')
