from .common import *

import dj_database_url

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l5c#ydi3r*17qj7537n@g89u)kx^yeu#w%ywz)jy*uul@@e1u1'

if os.environ.get('debug', False):
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = { 'default': dj_database_url.config() }

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

