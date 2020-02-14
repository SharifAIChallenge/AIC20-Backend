# Generated by Django 2.2.9 on 2020-02-14 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0021_tournament_finished'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='tournament_map',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='tournaments', to='challenge.Map'),
            preserve_default=False,
        ),
    ]
