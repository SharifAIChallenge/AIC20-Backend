# Generated by Django 2.2.9 on 2020-03-11 20:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0051_lobby_challenge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='challenge.Group'),
        ),
    ]
