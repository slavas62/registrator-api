# coding: utf-8

import os
import sys
import dj_database_url

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
ENV_DIR = os.path.join(os.path.dirname(sys.executable), '..')
LOG_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', '.log'))
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


SECRET_KEY = '%s5+l6&^f(x2c1q17bn)zgn_zrbhlv$h=4871#af8ij9+jrp4a'


DEBUG = False
DEBUG_SQL = False

ALLOWED_HOSTS = ['*']


APPS = [
    # 'acc',
    'userlayers_admin',
    'main',
]

USERLAYERS_APPS = [
    'mutant',
    'mutant.contrib.boolean',
    'mutant.contrib.file',
    'mutant.contrib.geo',
    'mutant.contrib.numeric',
    'mutant.contrib.related',
    'mutant.contrib.temporal',
    'mutant.contrib.text',
    'mutant.contrib.web',
    'userlayers',
]

INSTALLED_APPS = APPS + [
    'south',
    'suit',
    'django.contrib.gis',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sorl.thumbnail',
    'tastypie'
] + USERLAYERS_APPS

ROOT_URLCONF = 'main.urls'

WSGI_APPLICATION = 'wsgi.application'


LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = False

FIRST_DAY_OF_WEEK = 1

STATIC_URL = '/s/'
STATIC_ROOT = os.path.join(ENV_DIR, 'www', 'static')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_URL = '/m/'
MEDIA_ROOT = os.path.join(ENV_DIR, 'www', 'media')
if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# AUTH_USER_MODEL = 'acc.User'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'userlayers_admin.contrib.request_middleware.RequestMiddleware',
]

TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
]

# TASTYPIE SETTINGS
TASTYPIE_DEFAULT_FORMATS = ['json']
API_LIMIT_PER_PAGE = 100


SUIT_CONFIG = {
    'SEARCH_URL': '',
    'ADMIN_NAME': 'REGISTRATOR API',
    'LIST_PER_PAGE': 50,
    'SHOW_REQUIRED_ASTERISK': True,
    'MENU': [
        {'label': u'Пользователи', 'icon': 'icon-user', 'models': ('auth.user', 'auth.group')},
        {'label': u'Объекты', 'icon': 'icon-hdd', 'app': 'objects'},
        {'label': u'Модели', 'icon': 'icon-book', 'app': 'main'},
        {'label': u'Поля', 'icon': 'icon-list', 'app': 'mutant'},
    ],
}

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': ''
}

RESOURCE_FOLDER_IN_MEDIA_ROOT = 'resource'
RESOURCE_FOLDER_IMAGES_IN_MEDIA_ROOT = os.path.join(RESOURCE_FOLDER_IN_MEDIA_ROOT, 'image')
THUMBNAIL_PREFIX = os.path.join(RESOURCE_FOLDER_IMAGES_IN_MEDIA_ROOT, 'cache/')
RESOURCE_FOLDER_VIDEOS_IN_MEDIA_ROOT = os.path.join(RESOURCE_FOLDER_IN_MEDIA_ROOT, 'video')
RESOURCE_IMAGE_THUMBNAILS = [
    {'name': '200x200', 'geometry_string': '200x200', 'upscale': True},
    {'name': '600', 'geometry_string': '600'},
]
ICON_FOLDER_IN_MEDIA_ROOT = os.path.join(RESOURCE_FOLDER_IN_MEDIA_ROOT, 'icon')
THUMBNAIL_UPSCALE = False
THUMBNAIL_QUALITY = 100

USERLAYERS_MD_PERMISSION_STRATEGY = 2
USERLAYERS_MD_MODEL = 'main.MainModelDef'
# USERLAYERS_MD_CLASS_RESERVED_NAMES = ['image', 'video']
USERLAYERS_ADMIN_MD_CLASS = 'main.admin.MainModelDefinitionAdmin'
USERLAYERS_ADMIN_MD_OBJECT_CLASS = 'main.admin.MainModelDefinitionObjectAdmin'
USERLAYERS_API_TABLE_EXCLUDE_FIELDS = ['user_id', 'user']

DATABASES = {'default': dj_database_url.config(default='postgres://')}

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
