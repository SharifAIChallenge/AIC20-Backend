# Generated by Django 2.2.8 on 2020-02-02 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0011_auto_20200127_1245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='scoreboard',
        ),
    ]
