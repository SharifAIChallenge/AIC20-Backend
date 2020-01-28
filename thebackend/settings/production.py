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

LOG_ROOT = os.getenv('LOG_ROOT')

LOGGING = {
    'version': 1.0,
    'handlers': {
        'django_logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_ROOT + "/django.log",
            'maxBytes': 50000,
            'backupCount': 2,
        },
        'db_logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_ROOT + "/db.log",
            'maxBytes': 50000,
            'backupCount': 2,
        },
        'celery_logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_ROOT + "/celery.log",
            'maxBytes': 50000,
            'backupCount': 2,
        },
        'common_logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_ROOT + "/common.log",
            'maxBytes': 50000,
            'backupCount': 2,
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'django_logfile'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django.db.backends': {
            'handlers': ['console', 'db_logfile'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'celery.task': {
            'handlers': ['console', 'celery_logfile'],
            'level': 'DEBUG',
            'propagate': False,
        },
        '': {
            'handlers': ['common_logfile'],
            'propagate': True,
            'level': 'DEBUG',
        },

    }
}

TIME_ZONE = 'Iran'

STATIC_URL = '/static/'
STATIC_ROOT = '/files/aic/static'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/files/aic/media'

CSRF_COOKIE_HTTPONLY = True

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.getenv('EMAIL_PORT')
