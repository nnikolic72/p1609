__author__ = 'tanja'
from ConfigParser import ConfigParser
from unipath import Path

from squaresensor.settings.base import *

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
    'default': {
        'ENGINE': DATABASE_ENGINE,
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT,
    }
}

MEDIA_ROOT = PROJECT_DIR.child("media")
STATIC_ROOT = PROJECT_DIR.child("static")
MEDIA_URL = '/media/'
STATICFILES_DIRS = (
    PROJECT_DIR.child("assets"),
)


DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += ('debug_toolbar',)