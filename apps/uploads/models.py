from django.db import models
from django.conf import settings

class FileUpload(models.Model):
    file = models.FileField(upload_to='admin_file_uploads')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name + ':\t' + settings.MEDIA_URL + self.file.name
