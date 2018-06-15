from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l5c#ydi3r*17qj7537n@g89u)kx^yeu#w%ywz)jy*uul@@e1u1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

