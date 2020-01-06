from __future__ import absolute_import, unicode_literals
import os
from logging.config import dictConfig

from django.conf import settings
from celery import Celery
from celery.signals import setup_logging

""" RabbitMQ as message broker
"""

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thebackend.settings.development')
app = Celery(main='thebackend')
app.config_from_object('django.conf:settings')


@setup_logging.connect
def config_loggers(*args, **kwags):
    dictConfig(settings.LOGGING)


app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

