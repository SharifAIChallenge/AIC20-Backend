# Generated by Django 2.2.9 on 2020-02-09 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0004_notification_create_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='for_all',
        ),
    ]
