from django.db import models


class FileUpload(models.Model):
    file = models.FileField(upload_to='admin_file_uploads')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name + ':\t' + self.file.name
