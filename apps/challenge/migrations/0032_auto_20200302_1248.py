# Generated by Django 2.2.9 on 2020-03-02 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0031_matchteam_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchteam',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
