from bull.settings.base import *

DEBUG = False

MEDIA_URL = "/media/"
MEDIA_ROOT = "/srv/lafteweb/media_root"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'lafteweb',
        'USER': 'lafteweb',
        'PASSWORD': os.environ.get('LAFTEWEB_DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '',                      # Set to empty string for default.
    }
}