# coding: utf-8

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, '..', '..', '.log')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


SECRET_KEY = '%s5+l6&^f(x2c1q17bn)zgn_zrbhlv$h=4871#af8ij9+jrp4a'


DEBUG = False
DEBUG_SQL = False

ALLOWED_HOSTS = ['*']


APPS = [
    'acc',
    'main'
]

USERLAYERS_APPS = [
    'mutant',
    'mutant.contrib.boolean',
    'mutant.contrib.numeric',
    'mutant.contrib.text',
    'mutant.contrib.geo',
    'userlayers',
]

INSTALLED_APPS = [
    'south',
    'suit',
    'django.contrib.gis',
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
] + APPS + USERLAYERS_APPS


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'main.urls'

WSGI_APPLICATION = 'wsgi.application'


LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = False

FIRST_DAY_OF_WEEK = 1

STATIC_URL = '/s/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_prepared')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]

MEDIA_URL = '/m/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
ADMIN_MEDIA_PREFIX = STATIC_URL + "admin/"

AUTH_USER_MODEL = 'acc.User'
LOGIN_URL = '/acc/login'
LOGOUT_URL = '/acc/logout'
LOGIN_REDIRECT_URL = '/'

# TASTYPIE SETTINGS
TASTYPIE_DEFAULT_FORMATS = ['json']
API_LIMIT_PER_PAGE = 100


SUIT_CONFIG = {
    'SEARCH_URL': '',
    'ADMIN_NAME': 'REGISTRATOR API'
}

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': ''
}


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'registrator_api',
        'HOST': '127.0.0.1',
        'USER': 'postgres',
        'PASSWORD': '12345',
        'PORT': '5432',
    },
}


try:
    from registrator.config import *
except ImportError:
    pass


from .log import LOGGING


TEMPLATE_DEBUG = DEBUG
ENABLE_DEBUG_TOOLBAR = DEBUG


if ENABLE_DEBUG_TOOLBAR:
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += (
        'debug_toolbar',
        'django_extensions',
    )

if DEBUG_SQL:
    LOGGING['loggers']['django.db.backends'] = {
        'handlers': ['db_color_no_level'],
        'level': 'DEBUG',
    }
