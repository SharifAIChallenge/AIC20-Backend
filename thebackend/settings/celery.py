import os
from celery import Celery
from django.conf import settings

""" RabbitMQ as message broker
"""

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thebackend.settings.development')

app = Celery(main='thebackend')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
