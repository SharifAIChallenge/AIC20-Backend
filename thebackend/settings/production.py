import os

from .development import *


SECRET_KEY = 'oaeu#@$puoeuj,#$>Ueok,4IY@#$"PU.ohukAEOUO>AYU34$IPK'

DEBUG = False

ALLOWED_HOSTS = ['*']

WSGI_APPLICATION = 'thebackend.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv('DB_NAME'),
        "USER": os.getenv('DB_USER'),
        "PASSWORD": os.getenv('DB_PASSWORD'),
        "HOST": os.getenv('DB_HOST'),
        "PORT": os.getenv('DB_PORT'),
    }
}

TIME_ZONE = 'Iran'

STATIC_URL = '/static/'
STATIC_ROOT = '/static'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/media'

CSRF_COOKIE_HTTPONLY = True

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.getenv('EMAIL_PORT')

