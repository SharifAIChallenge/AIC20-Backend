# Generated by Django 2.2.8 on 2020-01-27 09:32

import apps.challenge.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0007_auto_20200126_1222'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submission',
            old_name='submit_date',
            new_name='submit_time',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='type',
        ),
        migrations.AddField(
            model_name='map',
            name='infra_token',
            field=models.CharField(max_length=256, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='map',
            name='name',
            field=models.CharField(default=None, max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='file',
            field=models.FileField(default=None, upload_to=apps.challenge.models.get_submission_file_directory),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='infra_compile_message',
            field=models.CharField(blank=True, max_length=1023, null=True),
        ),
        migrations.AddField(
            model_name='submission',
            name='infra_compile_token',
            field=models.CharField(blank=True, max_length=256, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='submission',
            name='infra_token',
            field=models.CharField(blank=True, max_length=256, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='submission',
            name='is_final',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='submission',
            name='language',
            field=models.CharField(choices=[('cpp', 'C++'), ('java', 'Java'), ('py3', 'Python 3'), ('go', 'Go')], default='java', max_length=50),
        ),
        migrations.AddField(
            model_name='submission',
            name='status',
            field=models.CharField(choices=[('uploading', 'Uploading'), ('uploaded', 'Uploaded'), ('compiling', 'Compiling'), ('compiled', 'Compiled'), ('failed', 'Failed')], default='uploading', max_length=50),
        ),
    ]
