from bull.settings.base import *

DEBUG = False

MEDIA_URL = "/media/"
MEDIA_ROOT = "/srv/lafteweb/media"

STATIC_URL = "/static/"
STATIC_ROOT = "/srv/lafteweb/static"

ALLOWED_HOSTS = ('lafteweb.ludvigjordet.com',)

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
