# Generated by Django 2.2.9 on 2020-02-08 21:14

import apps.participation.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participation', '0008_auto_20200202_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='image',
            field=models.ImageField(null=True, upload_to=apps.participation.models.Team.get_team_image_directory),
        ),
    ]
