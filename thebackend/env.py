DJANGO_SETTINGS_MODULE = 'thebackend.settings.production'

DB_NAME = 'AIC2020'
DB_USER = 'aic'
DB_PASSWORD = '@ich@llenge2o2ow!llbefunenough'
DB_HOST = 'localhost'
DB_PORT = '5432'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'sharif.aichallenge@gmail.com'
EMAIL_HOST_PASSWORD = 'aichallenge_SSC_96'
EMAIL_PORT = '587'

LOG_ROOT = '/var/log/thebackend/'

