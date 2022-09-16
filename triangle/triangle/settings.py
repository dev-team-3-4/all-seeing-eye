"""
Environ Variables:
    Django:
        DEBUG:
            int: 0-False, 1-True
            default: 0
        HANDLE_EXCEPTIONS
            int: 0-False, 1-True
            default: not DEBUG

    Database:
        DB_NAME
            string
        DB_USER
            string
            default: postgres
        DB_PASSWORD
            string
        DB_HOST
            string
            default: '127.0.0.1'
        DB_PORT
            int
            default: 5432

    email:
        EMAIL_HOST_USER:
            :type: str | None
            :default: None
        EMAIL_HOST_PASSWORD:
            :type: str | None
            :default: None

    blockchain:
        BANK_ADDRESS:
            :type: str | None
            :default: None
        BANK_PRIVATE_KEY:
            :type: str | None
            :default: None
        BLOCKCHAIN_RPC_URL:
            :type: str | None
            :default: None
        BLOCKCHAIN_TOKEN_ADDRESS:
            :type: str | None
            :default: None
        OUTPUT_GAS_COUNT:
            :type: int | None
            :default: 0
"""
import os
from os import environ, path
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-e0^j=7m#!w7iy48#3hp&!sr%l*45y+i)&*5n$8-7&mr8k@p!mt'
DEBUG = bool(int(environ.setdefault('DEBUG', '0')))
HANDLE_EXCEPTIONS = bool(int(environ['HANDLE_EXCEPTIONS'])) if 'HANDLE_EXCEPTIONS' in environ else not DEBUG

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'drf_spectacular',
    'rest_framework.authtoken',
    'rest_framework',

    'frontend.apps.FrontConfig',
    'users.apps.UsersConfig',
    'chats.apps.ChatsConfig',
    'contracts.apps.ContractsConfig',
    'payments'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'triangle.urls'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'users.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ],

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema'
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'triangle.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': environ['DB_NAME'],
        'USER': environ.setdefault('DB_USER', 'postgres'),
        'PASSWORD': environ['DB_PASSWORD'],
        'HOST': environ.setdefault('DB_HOST', 'localhost'),
        'PORT': environ.setdefault('DB_PORT', '5432'),
    }
}

AUTH_USER_MODEL = 'users.User'

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

###
# email

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD')

# email
###

###
# blockchain

BANK_ADDRESS = environ.get('BANK_ADDRESS')
BANK_PRIVATE_KEY = environ.get('BANK_PRIVATE_KEY')
BLOCKCHAIN_RPC_URL = environ.get('BLOCKCHAIN_RPC_URL')
BLOCKCHAIN_TOKEN_ADDRESS = environ.get('BLOCKCHAIN_TOKEN_ADDRESS')
OUTPUT_GAS_COUNT = int(environ.get('OUTPUT_GAS_COUNT')) if environ.get('OUTPUT_GAS_COUNT') else 0

# blockchain
###

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
STATIC_URL = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = [
    BASE_DIR / "frontend/static",
]


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
