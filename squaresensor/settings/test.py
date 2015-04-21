__author__ = 'tanja'
from squaresensor.settings.base import *
import os
import dj_database_url

#Heroku deployment

#from memcacheify import memcacheify  # @UnresolvedImport
#CACHES = memcacheify()


config = ConfigParser()
settings_path = PROJECT_DIR.child('squaresensor').child("settings")
settings_path = Path(settings_path, 'settings.ini')
config.read(settings_path)

SECRET_KEY = config.get('squaresensor', 'APP_SECRET_KEY')
DATABASE_USER = config.get('database', 'DATABASE_USER')
DATABASE_PASSWORD = config.get('database', 'DATABASE_PASSWORD')
DATABASE_HOST = config.get('database', 'DATABASE_HOST')
DATABASE_PORT = config.get('database', 'DATABASE_PORT')
DATABASE_ENGINE = config.get('database', 'DATABASE_ENGINE')
DATABASE_NAME = config.get('database', 'DATABASE_NAME')


#INSTAGRAM_API_KEY = config.get('instagram', 'INSTAGRAM_API_KEY')


DATABASES = {
"default": {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": ":memory:",
    "USER": "",
    "PASSWORD": "",
    "HOST": "",
    "PORT": "",
    },
}


MEDIA_ROOT = PROJECT_DIR.child("media")
STATIC_ROOT = PROJECT_DIR.child("static")
MEDIA_URL = '/media/'
STATICFILES_DIRS = (
    PROJECT_DIR.child("assets"),
)


DEBUG = True

TEMPLATE_DEBUG = True



INSTALLED_APPS += ('debug_toolbar',)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ALLOWED_HOSTS = ['*']

MIDDLEWARE_CLASSES += ('django.middleware.clickjacking.XFrameOptionsMiddleware',)


