# Generated by Django 2.2.8 on 2020-01-26 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0005_auto_20200124_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='type',
            field=models.CharField(choices=[('primary', 'Primary Challenge'), ('final', 'Finale Challenge')], max_length=50),
        ),
    ]
