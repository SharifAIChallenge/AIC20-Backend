# Generated by Django 2.2.8 on 2020-01-24 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoreboard', '0002_auto_20200124_0930'),
    ]

    operations = [
        migrations.AddField(
            model_name='row',
            name='score',
            field=models.FloatField(default=1000.0),
        ),
    ]
