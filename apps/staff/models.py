from django.db import models


# Create your models here.

class Staff(models.Model):
    group_title = models.CharField(max_length=128)
    team_title = models.CharField(max_length=256, default='_')
    first_name_en = models.CharField(max_length=128)
    first_name_fa = models.CharField(max_length=128)
    last_name_en = models.CharField(max_length=128)
    last_name_fa = models.CharField(max_length=128)
    url = models.CharField(max_length=500)

    def upload_path(self, filename):
        return f'staff/{self.group_title}/{self.team_title}/{filename}'

    image = models.ImageField(upload_to=upload_path)
