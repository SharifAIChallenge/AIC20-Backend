bind = ''
workers = 4
proc_name = 'datadays gunicorn'
preload=True
timeout=30
user = 'root'
group = 'root'
loglevel = 'debug'
errorlog = ''
raw_env = [
        'DJANGO_SETTINGS_MODULE=thebackend.settings.production',

        'DB_NAME',
        'DB_USER',
        'DB_PASSWORD',
        'DB_HOST',
        'DB_PORT',

        'EMAIL_BACKEND',
        'EMAIL_USE_TLS',
        'EMAIL_HOST',
        'EMAIL_HOST_USER',
        'EMAIL_HOST_PASSWORD',
        'EMAIL_PORT',

        'LOG_ROOT',
]

