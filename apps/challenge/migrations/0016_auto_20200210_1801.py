# Generated by Django 2.2.9 on 2020-02-10 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0015_auto_20200202_1552'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tournament',
            old_name='end_time',
            new_name='submit_deadline',
        ),
        migrations.AlterField(
            model_name='tournament',
            name='start_time',
            field=models.DateTimeField(),
        ),
    ]
