from __future__ import absolute_import
"""
Django settings for squaresensor project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

import re
import os
from os import environ
from unipath import Path
from ConfigParser import ConfigParser
import djcelery
djcelery.setup_loader()

PROJECT_DIR = Path(__file__).ancestor(3)
BASE_DIR = PROJECT_DIR.child('squaresensor')


config = ConfigParser()
settings_path = PROJECT_DIR.child('squaresensor').child("settings")
settings_path = Path(settings_path, 'settings.ini')
config.read(settings_path)

INSTAGRAM_AUTH_EXTRA_ARGUMENTS = {'scope': 'likes comments relationships'}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

try:
    PAYPAL_TEST_ENV = os.environ['PAYPAL_TEST']
except:
    PAYPAL_TEST_ENV = None
if not PAYPAL_TEST_ENV:
    try:
        PAYPAL_TEST_ENV = config.get('squaresensor', 'PAYPAL_TEST')
    except:
        PAYPAL_TEST_ENV = None

PAYPAL_TEST = True
if PAYPAL_TEST_ENV:
    if PAYPAL_TEST_ENV == '1':
        PAYPAL_TEST = True

    if PAYPAL_TEST_ENV == '0':
        PAYPAL_TEST = False
else:
    PAYPAL_TEST = True


try:
    PAYPAL_RECEIVER_EMAIL = os.environ['PAYPAL_RECEIVER_EMAIL']
except:
    PAYPAL_RECEIVER_EMAIL = None
if not PAYPAL_RECEIVER_EMAIL:
    try:
        PAYPAL_RECEIVER_EMAIL = config.get('squaresensor', 'PAYPAL_RECEIVER_EMAIL')
    except:
        PAYPAL_RECEIVER_EMAIL = None

try:
    ROOT_SITE_URL = os.environ['ROOT_SITE_URL']
except:
    ROOT_SITE_URL = None
if not ROOT_SITE_URL:
    try:
        ROOT_SITE_URL = config.get('squaresensor', 'ROOT_SITE_URL')
    except:
        ROOT_SITE_URL = None

try:
    IS_PAYMENT_LIVE = os.environ['IS_PAYMENT_LIVE']
except:
    IS_PAYMENT_LIVE = None
if not IS_PAYMENT_LIVE:
    try:
        IS_PAYMENT_LIVE = config.get('squaresensor', 'IS_PAYMENT_LIVE')
    except:
        IS_PAYMENT_LIVE = None

try:
    INSTAGRAM_COMMENTS_ALLOWED = os.environ['INSTAGRAM_COMMENTS_ALLOWED']
except:
    INSTAGRAM_COMMENTS_ALLOWED = None
if not INSTAGRAM_COMMENTS_ALLOWED:
    try:
        INSTAGRAM_COMMENTS_ALLOWED = config.get('instagram', 'INSTAGRAM_COMMENTS_ALLOWED')
    except:
        INSTAGRAM_COMMENTS_ALLOWED = None

try:
    INSTAGRAM_CLIENT_ID = os.environ['CLIENT_ID']
except:
    INSTAGRAM_CLIENT_ID = None
if not INSTAGRAM_CLIENT_ID:
    try:
        INSTAGRAM_CLIENT_ID = config.get('instagram', 'CLIENT_ID')
    except:
        INSTAGRAM_CLIENT_ID = None

try:
    INSTAGRAM_CLIENT_SECRET = os.environ['CLIENT_SECRET']
except:
    INSTAGRAM_CLIENT_SECRET = None
if not INSTAGRAM_CLIENT_SECRET:
    try:
        INSTAGRAM_CLIENT_SECRET = config.get('instagram', 'CLIENT_SECRET')
    except:
        INSTAGRAM_CLIENT_SECRET = None

try:
    INSTAGRAM_REDIRECT_URI = os.environ['INSTAGRAM_REDIRECT_URI']
except:
    INSTAGRAM_REDIRECT_URI = None
if not INSTAGRAM_REDIRECT_URI:
    try:
        INSTAGRAM_REDIRECT_URI = config.get('instagram', 'INSTAGRAM_REDIRECT_URI')
    except:
        INSTAGRAM_REDIRECT_URI = None

try:
    INSTAGRAM_SECRET_KEY = os.environ['INSTAGRAM_SECRET_KEY']
except:
    INSTAGRAM_SECRET_KEY = None
if not INSTAGRAM_SECRET_KEY:
    try:
        INSTAGRAM_SECRET_KEY = config.get('instagram', 'INSTAGRAM_SECRET_KEY')
    except:
        INSTAGRAM_SECRET_KEY = None

try:
    INSTAGRAM_SECRET_KEY = os.environ['INSTAGRAM_SECRET_KEY']
except:
    INSTAGRAM_SECRET_KEY = None
if not INSTAGRAM_SECRET_KEY:
    try:
        INSTAGRAM_SECRET_KEY = config.get('instagram', 'INSTAGRAM_SECRET_KEY')
    except:
        INSTAGRAM_SECRET_KEY = None

# RabbitMQ URI
try:
    BROKER_URL = os.environ['RABBITMQ_BIGWIG_TX_URL']
except:
    BROKER_URL = None
if not BROKER_URL:
    try:
        BROKER_URL = config.get('rabbitmq', 'BROKER_URL')
    except:
        BROKER_URL = None

try:
    CELERY_RESULT_BACKEND = os.environ['RABBITMQ_BIGWIG_RX_URL']
except:
    CELERY_RESULT_BACKEND = None
if not BROKER_URL:
    try:
        CELERY_RESULT_BACKEND = config.get('rabbitmq', 'CELERY_RESULT_BACKEND')
    except:
        CELERY_RESULT_BACKEND = None

BROKER_POOL_LIMIT = 1

try:
    IS_APP_LIVE = environ.get('IS_APP_LIVE')
except:
    IS_APP_LIVE = None
if not IS_APP_LIVE:
    try:
        IS_APP_LIVE = config.get('squaresensor', 'IS_APP_LIVE')
    except:
        IS_APP_LIVE = None


# Application definition

INSTALLED_APPS = (
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'dajaxice',
    'import_export',
    'bootstrap3',
    'social_auth',
    'djcelery',
    'crispy_forms',
    'emoji',
    'paypal.standard.ipn',

    'lander',
    'instagramuser',
    'members',
    'attributes',
    'categories',
    'photos',
    'smartfeed',
    'hashtags',
    'ads',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'squaresensor.urls'

WSGI_APPLICATION = 'squaresensor.wsgi.application'


#Celery configurations
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'



# Templates
TEMPLATE_DIRS = (
    PROJECT_DIR.child("templates"),
    PROJECT_DIR.child("templates").child("squaresensor"),
                 )

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)


AUTHENTICATION_BACKENDS = (
    'social_auth.backends.contrib.instagram.InstagramBackend',
    'django.contrib.auth.backends.ModelBackend',
)


SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    #'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.user.get_username',
    'social_auth.backends.pipeline.user.create_user',
    'squaresensor.pipeline.add_member',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details',
)

LOGIN_URL = '/'
LOGOUT_URL = '/members/logout'
LOGIN_REDIRECT_URL = '/members/dashboard'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#Set this to True to include language selectors
SHOW_TRANSLATIONS = False

LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('en', 'English'),
    ('de', 'German'),
    ('es', 'Spanish'),
)

LOCALE_PATHS = (
    PROJECT_DIR.child("locale"),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'dajaxice.finders.DajaxiceFinder',
)

STATIC_URL = '/static/'

IGNORABLE_404_URLS = (
    re.compile(r'^/apple-touch-icon.*\.png$'),
    re.compile(r'^/favicon\.ico$'),
    re.compile(r'^/robots\.txt$'),
)

# Bootstrap admin settings
DAB_FIELD_RENDERER = 'django_admin_bootstrapped.renderers.BootstrapFieldRenderer'

from django.contrib import messages

MESSAGE_TAGS = {
            messages.SUCCESS: 'alert-success success',
            messages.WARNING: 'alert-warning warning',
            messages.ERROR: 'alert-danger error'
}

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Squaresensor globals -------------------------------------------------------


#GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-14845987-3'
#GOOGLE_ANALYTICS_DOMAIN = 'squaresensor.com'

TEST_APP = True
#Used for testing
TEST_APP_FRIENDS_TR_ANALYZE_N_FRIENDS = 199
TEST_APP_FRIENDS_TR_ANALYZE_N_FOLLOWINGS = 299
TEST_APP_LIKE_PER_PERIOD_LIMIT = 60
TEST_APP_COMMENT_PER_PERIOD_LIMIT = 60

# Squaresensor Membership Prices
SQUARESENSOR_MONTHLY_MEMBERSHIP = 4.95
SQUARESENSOR_YEARLY_MEMBERSHIP = 49.95

# Instgram limits for signed calls
INSTAGRAM_LIKES_PER_HOUR_LIMIT = 60
INSTAGRAM_COMMENTS_PER_HOUR_LIMIT = 60
INSTAGRAM_LIMIT_PERIOD_RESET_TIME_HOURS = 1  # when Instagram resets their limits

# Commenting parameters
COMMENTER_NO_OF_PICS_NON_MEMBER_LIMIT = 10
COMMENTER_NO_OF_PICS_MEMBER_LIMIT = 30

# Find New Friends parameters
FIND_NEW_FRIENDS_MAX_NON_MEMBER_DAILY_INTERACTIONS = 10
FIND_NEW_FRIENDS_MAX_MEMBER_DAILY_INTERACTIONS = 50
FIND_FRIENDS_LIMIT_PERIOD_RESET_TIME_DAYS = 1

# APP settings: inpiring users
INSPIRING_USERS_FIND_TOP_N_PHOTOS = 10  # how may best photos to find
INSPIRING_USERS_SEARCH_N_PHOTOS = 500  # how many last photos to search while finding the best ones

# APP settings: followings
FOLLOWINGS_FIND_TOP_N_PHOTOS = 10  # how may best photos to find
FOLLOWINGS_SEARCH_N_PHOTOS = 500  # how many last photos to search while finding the best ones

# APP settings: friends/followers
FRIENDS_FIND_TOP_N_PHOTOS = 4  # how may best photos to find
FRIENDS_SEARCH_N_PHOTOS = 100  # how many last photos to search while finding the best ones

# APP settings: members
MEMBERS_FIND_TOP_N_PHOTOS = 20  # how may best photos to find
MEMBERS_SEARCH_N_PHOTOS = 1000  # how many last photos to search while finding the best ones

# Friends inclusion thresholds
FRIENDS_TR_ANALYZE_N_FRIENDS = 1000
FRIENDS_TR_LAST_POST_BEFORE_DAYS = 2
FRIENDS_TR_MIN_MEDIA_COUNT = 50
FRIENDS_TR_MAX_MEDIA_COUNT = float("inf")
FRIENDS_TR_MIN_FOLLOWINGS = 100
FRIENDS_TR_MAX_FOLLOWINGS = 900
FRIENDS_TR_MIN_FOLLOWERS = 200
FRIENDS_TR_MAX_FOLLOWERS = 800
FRIENDS_TR_MIN_FF_RATIO = 0.85
FRIENDS_TR_MAX_FF_RATIO = 4

# Followings inclusion thresholds
FOLLOWINGS_TR_ANALYZE_N_FOLLOWINGS = 1000
FOLLOWINGS_TR_LAST_POST_BEFORE_DAYS = 30
FOLLOWINGS_TR_MIN_MEDIA_COUNT = 50
FOLLOWINGS_TR_MAX_MEDIA_COUNT = float("inf")
FOLLOWINGS_TR_MIN_FOLLOWINGS = float("-inf")
FOLLOWINGS_TR_MAX_FOLLOWINGS = float("+inf")
FOLLOWINGS_TR_MIN_FOLLOWERS = 100
FOLLOWINGS_TR_MAX_FOLLOWERS = float("+inf")
FOLLOWINGS_TR_MIN_FF_RATIO = float("-inf")
FOLLOWINGS_TR_MAX_FF_RATIO = 1.5

#General threshold - when to stop processing Instagram requests
INSTAGRAM_API_THRESHOLD = 500

# SmartFeed
IMPORT_MAX_INSTAGRAM_FOLLOWINGS = 2000
IMPORT_MAX_INSTAGRAM_FOLLOWERS = 10000

SMART_FEED_BATCH_SIZE = 20
SMART_FEED_MAX_LOAD_PICS = 2000

MIN_SQUAREFOLLOWINGS = 15
MAX_SQUAREFOLLOWINGS = 2000