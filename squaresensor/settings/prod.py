__author__ = 'tanja'
from squaresensor.settings.base import *

#Heroku deployment
import os
import dj_database_url

from memcacheify import memcacheify  # @UnresolvedImport
CACHES = memcacheify()

#Prod environment settings

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False

TEMPLATE_DEBUG = False


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '../../static'),
)
DATABASES = {
    'default': dj_database_url.config(default='sqlite:///db.sqlite')
}
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ALLOWED_HOSTS = ['*']

MIDDLEWARE_CLASSES += ('django.middleware.clickjacking.XFrameOptionsMiddleware',)

