from django.db import models


# Create your models here.

class Staff(models.Model):
    title = models.CharField(max_length=256)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    url = models.CharField(max_length=500)

    def upload_path(self, filename):
        return f'staff/{self.title}/{filename}'

    image = models.FileField(upload_to=upload_path)
