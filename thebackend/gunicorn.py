bind = '0.0.0.0:8000'

workers = 4
proc_name = 'aic gunicorn'

preload=True
timeout=60

loglevel = 'debug'

errorlog = '/var/log/thebackend/gunicorn_error.log'
