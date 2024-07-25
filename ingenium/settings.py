"""
Django settings for ingenium project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import enum

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-wxv1_i05jibw7wz%h3%4_%e9n1a^h8mfo$_)+_j4-hhw)fwq%="

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True 

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'users.apps.UsersConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'debug_toolbar',

    'crispy_forms', 
    'crispy_bootstrap4',

    # 'users',
    'questions', 
    'votes',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

SITE_ID = 2

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ingenium.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'ingenium.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'), 
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'), 
        'HOST': "localhost", 
        'PORT': "5439" 
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache', 
        'LOCATION': 'redis://127.0.0.1:6390',
    }
}

class CacheKeys(): 

    class Static(enum.Enum): 
        ALL_CATEGORIES: str = 'cache:all_categories'
        ALL_CATEGORIES_WITH_TAGS: str = 'cache:all_categories_with_tags'
        ALL_QUESTIONS: str = 'cache:all_questions'

    class Dynamic():
        @staticmethod
        def category(slug: str) -> str: 
            return f'category:{slug}'
        
        @staticmethod
        def questions_by_category(category_slug: str) -> str: 
            return f'category:{category_slug}:questions'
        
        @staticmethod 
        def single_question(year: int, month: int, day: int, question_slug: str) -> str: 
            return f'question:{year}_{month}_{day}_{question_slug}'
        
        @staticmethod 
        def similar_questions(year: int, month: int, day: int, question_slug: str) -> str: 
            return f'question:{year}_{month}_{day}_{question_slug}'
    

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru-Ru'

TIME_ZONE = 'Asia/Novosibirsk' 

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]  

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Auth
AUTH_USER_MODEL = 'users.User'
LOGIN_URL = '/users/login'


# Media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# SMTP
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'sergegnabri2005@gmail.com'
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'sergegnabri2005@gmail.com'


# Redis 
REDIS_HOST = '127.0.0.1' 
REDIS_PORT = '6390' 

# Celery
CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0' 
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600} 
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0' 
CELERY_ACCEPT_CONTENT = ['application/json'] 
CELERY_TASK_SERIALIZER = 'json' 
CELERY_RESULT_serializer = 'json' 
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True


INTERNAL_IPS = [
    '127.0.0.1',
]