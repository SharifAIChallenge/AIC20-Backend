# Generated by Django 2.2.9 on 2020-03-08 17:40

import apps.challenge.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0048_group_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameteam',
            name='log',
            field=models.FileField(blank=True, max_length=1024, null=True, upload_to=apps.challenge.models.GameTeam.team_single_game_log),
        ),
    ]
