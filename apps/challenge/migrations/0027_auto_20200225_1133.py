# Generated by Django 2.2.9 on 2020-02-25 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0026_lobby_with_friend'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='code_submit_delay',
            field=models.IntegerField(default=5),
        ),
        migrations.AddField(
            model_name='challenge',
            name='friendly_game_delay',
            field=models.IntegerField(default=5),
        ),
    ]
