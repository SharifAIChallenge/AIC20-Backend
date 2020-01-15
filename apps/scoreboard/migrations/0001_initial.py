# Generated by Django 2.2.8 on 2020-01-15 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('participation', '0001_initial'),
        ('challenge', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Row',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ScoreBoard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='scoreboard', to='challenge.Stage')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scoreboards', to='challenge.Tournament')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.FloatField(default=1000.0)),
                ('row', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='score', to='scoreboard.Row')),
            ],
        ),
        migrations.AddField(
            model_name='row',
            name='scoreboard',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rows', to='scoreboard.ScoreBoard'),
        ),
        migrations.AddField(
            model_name='row',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rows', to='participation.Participant'),
        ),
    ]
