# Generated by Django 2.2.8 on 2020-01-27 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participation', '0005_auto_20200127_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='badges',
            field=models.ManyToManyField(blank=True, null=True, related_name='teams', to='participation.Badge'),
        ),
    ]
