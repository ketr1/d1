import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = 'django-insecure-key-change-in-production'

DEBUG = True

ALLOWED_HOSTS = [
    "d1-lyart-ten.vercel.app",
    ".vercel.app",
    "localhost",
    "127.0.0.1",
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'recipes.apps.RecipesConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'recipes.middleware.RestoreMissingUserMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'wsgi.application'

SOURCE_DB = BASE_DIR / 'db.sqlite3'

if os.environ.get('VERCEL') == '1':
    TMP_DB = Path('/tmp/db.sqlite3')

    if SOURCE_DB.exists() and not TMP_DB.exists():
        shutil.copyfile(SOURCE_DB, TMP_DB)

    DB_NAME = TMP_DB
else:
    DB_NAME = SOURCE_DB

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_NAME,
    }
}

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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'

SOURCE_MEDIA_ROOT = BASE_DIR / 'media'

if os.environ.get('VERCEL') == '1':
    MEDIA_ROOT = Path('/tmp/media')

    if SOURCE_MEDIA_ROOT.exists():
        shutil.copytree(
            SOURCE_MEDIA_ROOT,
            MEDIA_ROOT,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns('*.zip'),
        )
else:
    MEDIA_ROOT = SOURCE_MEDIA_ROOT

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

SESSION_COOKIE_NAME = 'healthy_food_session_v2'
SESSION_COOKIE_AGE = 1209600
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_PATH = '/'

CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'


SESSION_COOKIE_SECURE = os.environ.get('VERCEL') == '1'
CSRF_COOKIE_SECURE = os.environ.get('VERCEL') == '1'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
