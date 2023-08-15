"""
Django settings for vschools project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os.path
from decouple import config
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ADMINS = [
    ('Katumba Victor','katumbavictor5@gmail.com')
]

MANAGERS = ADMINS

ALLOWED_HOSTS = ['vschoolsmeet.tech','www.vschoolsmeet.tech','191.96.57.85','127.0.0.1','localhost',
                'dialogue.vschoolsmeet.tech', 'dialogue.localhost','www.localhost']

ROOT_URLCONF = f'{config("PROJECT_NAME")}.urls'
ROOT_HOSTCONF = f'{config("PROJECT_NAME")}.hosts'
DEFAULT_HOST = 'www'
PARENT_HOST = 'localhost'

ASGI_APPLICATION = f'{config("PROJECT_NAME")}.asgi.application'

# Application definition

INSTALLED_APPS = [
    'daphne',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'django_celery_results',
    'django_celery_beat',
    'compressor',
    'django_redis',
    'db_file_storage',
    'payments',
    'axes',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'djoser.webauthn',
    'django_hosts',
    'webpush',
    'vschoolschat'
]


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            'hosts': [('localhost', 6379)]
        },
    },
}

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
    'axes.middleware.AxesMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware'
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    "django.contrib.auth.backends.ModelBackend"
]

DJOSER = {
    'LOGIN_FIELD':'email',
    'SEND_ACTIVATION_EMAIL': True,
    'LOGOUT_ON_PASSWORD_CHANGE': True,
    'ACTIVATION_URL': 'verify-email/{uid}/{token}',
    'PASSWORD_RESET_CONFIRM_URL': 'reset/{uid}/{token}',
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': True,
    'USERNAME_RESET_SHOW_EMAIL_NOT_FOUND': True,
    'USER_CREATE_PASSWORD_RETYPE': True
}

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': {
        'rest_framework.authentication.TokenAuthenticatioin',
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    }
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

WSGI_APPLICATION = f'{config("PROJECT_NAME")}.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

#DEFAULT_FILE_STORAGE = 'db_file_storage.storage.DatabaseFileStorage'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

WEBPUSH_SETTINGS = {
    'VAPID_PUBLIC_KEY': 'BCA2I2ypilTvhTaHxbqzbCGDdBgkmLaM0ydsZXNpnoIPdIzf4Va8poLm-GlGJcMN4t8I29yOtCGSrvdA7EUMxJY',
    'VAPID_PRIVATE_KEY': 'fgjnXLr1f0yZbbqoHrfCK7Bf1EO97lYODuPyNEws-_U',
    'VAPID_ADMIN_EMAIL': 'katumbavictor5@gmail.com'
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": 'redis://127.0.0.1:6379',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SESSION_COOKIE_DOMAIN = '.localhost'
CSRF_COOKIE_DOMAIN = '.localhost'
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

cache_backend = 'default'

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/ 

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static files')]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

    'compressor.finders.CompressorFinder'
)

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login'
LOGOUT_REDIRECT_URL = '/login'

AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = timedelta(minutes=20)
AXES_LOCKOUT_TEMPLATE = 'lockout.html'

PAYMENT_HOST = 'localhost:8000'
PAYMENT_USES_SSL = False

COMPRESS_OFFLINE = False
COMPRESS_ENABLED = False
COMPRESS_CSS_HASHING_METHOD = 'content'
COMPRESS_FILTERS = {
    'css':[
        'compressor.filters.css_default.CssAbsoluteFilter',
        'compressor.filters.cssmin.rCSSMinFilter',
    ],
    'js':[
        'compressor.filters.jsmin.JSMinFilter',
    ]
}

HTML_MINIFY = True
KEEP_COMMENTS_ON_MINIFYING = True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

if not DEBUG:
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO','https')
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    COMPRESS_ENABLED = True

    PARENT_HOST = 'vschoolsmeet.tech'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config("DATABASE_NAME"),
            'USER': config("DATABASE_USER"),
            'PASSWORD': config("DATABASE_PASSWORD"),
            'HOST': config("DATABASE_HOST"),
            'PORT': config("DATABASE_PORT")
        }
    }

CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
accept_content = ['application/json']
result_serializer = 'json'
task_serializer = 'json'
timezone = 'Africa/Kampala'

result_backend = 'django-db'

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'