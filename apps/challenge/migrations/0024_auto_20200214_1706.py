# Generated by Django 2.2.9 on 2020-02-14 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0023_auto_20200214_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='type',
            field=models.CharField(choices=[('league', 'league'), ('hourly', 'hourly'), ('double elimination', 'double elimination')], default='hourly', max_length=20),
        ),
    ]
