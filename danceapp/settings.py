#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Django settings for danceapp project.

Generated by 'django-admin startproject' using Django 1.9.7.
"""

import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DANCEAPP_ENVIRONMENT = os.environ.get('DANCEAPP_ENVIRONMENT')
if DANCEAPP_ENVIRONMENT is None:
    LOCAL_DEVELOPMENT = True
else:
    LOCAL_DEVELOPMENT = False


try:
    SECRET_KEY
except NameError:
    SECRET_FILE = os.path.join(BASE_DIR, 'secret.key')
    try:
        SECRET_KEY = open(SECRET_FILE).read().strip()
    except IOError:
        try:
            import random
            valid_chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
            SECRET_KEY = ''.join([random.SystemRandom().choice(valid_chars)
                                 for i in range(50)])
            secret = open(SECRET_FILE, 'w')
            secret.write(SECRET_KEY)
            secret.close()
        except IOError:
            Exception('Please create a %s file with random characters \
            to generate your secret key!' % SECRET_FILE)

if LOCAL_DEVELOPMENT:
    DEBUG = True
    CROWLEY_LOGFILE = os.path.join(BASE_DIR, 'crowley_debug.log')
    ALLOWED_HOSTS = []
else:
    DEBUG = False
    CROWLEY_LOGFILE = '/var/log/danceapp/crowley.log'
    # ALLOWED_HOSTS = ['.danceapp.com.br']
    ALLOWED_HOSTS = ['*']


# Aplicações default do Django
DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Aplicações de terceiros
THIRD_PARTY_APPS = [
    'rest_framework',
]

# Aplicações de terceiros que precisam ser declaradas antes das default
PRIORITY_APPS = [
     'material',
     'material.admin',
]

# Aplicações deste projeto
LOCAL_APPS = [
    'backend',
    'crowley',
]

# Application definition
INSTALLED_APPS = PRIORITY_APPS + DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'danceapp.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'danceapp.wsgi.application'


if LOCAL_DEVELOPMENT:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    db_from_env = dj_database_url.config(conn_max_age=600)
    DATABASES['default'].update(db_from_env)
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.mysql',
    #         'NAME': os.environ.get('DANCEAPP_DBNAME'),
    #         'USER': os.environ.get('DANCEAPP_DBUSER'),
    #         'PASSWORD': os.environ.get('DANCEAPP_DBPASSWORD'),
    #         'HOST': os.environ.get('DANCEAPP_DBHOST'),
    #         'PORT': os.environ.get('DANCEAPP_DBPORT'),
    #     }
    # }


django_validation = 'django.contrib.auth.password_validation'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': django_validation + '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': django_validation + '.MinimumLengthValidator',
    },
    {
        'NAME': django_validation + '.CommonPasswordValidator',
    },
    {
        'NAME': django_validation + '.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')
STATIC_URL = '/static/'

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

