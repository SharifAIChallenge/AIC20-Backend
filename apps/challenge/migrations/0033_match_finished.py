# Generated by Django 2.2.9 on 2020-03-02 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0032_auto_20200302_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='finished',
            field=models.BooleanField(default=False),
        ),
    ]
