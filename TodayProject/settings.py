"""
Django settings for TodayProject project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '46x1@ythhko4@w%z4o749u7zub)qok!j6h1!-iizrgf6g(zaiu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = ['137.74.171.90','.enjoytoday.fr']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',
    'datetimewidget',
    'easy_maps',
    'imagekit',
    'topic.apps.TopicConfig',
    'connection.apps.ConnectionConfig',
    'core.apps.CoreConfig',
    'crud.apps.CrudConfig',
    'location.apps.LocationConfig',
    'django.contrib.sites',
    'widget.apps.WidgetConfig',
    'not_implemented.apps.NotImplementedConfig',

]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
]

ROOT_URLCONF = 'TodayProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #added :
                'TodayProject.context_processors.topic_sidebar',
                'TodayProject.context_processors.topic_list',
                'TodayProject.context_processors.city_name',
                'TodayProject.context_processors.sites',
		'TodayProject.context_processors.urls',

            ],
        },
    },
]

WSGI_APPLICATION = 'TodayProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
        'default': {

        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            #'read_default_file': os.path.join(BASE_DIR, 'devmy.cnf'),
            'read_default_file': '/home/devpay2/darkside/devmy.cnf',

        },
    }


}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

FILE_CHARSET = 'utf-8'

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

# do not use TZ so that each time is like datetime.now
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'core/static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'topic/media')
# modify this if not on the same computer to avoid error 500
MEDIA_URL = '/media/'

# Settings for django-bootstrap3
BOOTSTRAP3 = {
    'include_jquery': True,
}

SWINGTIME_SETTINGS_MODULE = 'topic.swingtime_settings'

EASY_MAPS_CENTER = (48.853, 2.35)

# to overwrite when we will properly separate login process from core
LOGIN_URL = ''

#Cache

#CACHES = {
#    'default': {
#        'BACKEND' : 'django.core.cache.backends.locmem.LocMemCache',
#        'LOCATION': 'path.to.location',
#        'TIMEOUT': 5,
#        'KEY_FUNCTION': '.utils.make_key_per_site',
#        'OPTIONS': {
#            'MAX_ENTRIES': 1000
#        }
#    }
#}
