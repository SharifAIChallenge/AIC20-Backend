import os

from .development import *


SECRET_KEY = 'b7=wz(h_fhvh%s8j)e*%zbd$4*fi-!e3g0kh&(3gbng%r8w8jq'

DEBUG = False

ALLOWED_HOSTS = ['*']

WSGI_APPLICATION = 'thebackend.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}

TIME_ZONE = 'Iran'

STATIC_URL = '/static/'
STATIC_ROOT = './statics'

MEDIA_URL = '/media/'
MEDIA_ROOT = './media'

CSRF_COOKIE_HTTPONLY = False
