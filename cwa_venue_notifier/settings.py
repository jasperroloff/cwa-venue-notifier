"""
Django settings for cwa_venue_notifier project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

from celery.schedules import crontab
from environ import environ


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    SECRET_KEY=(str, ''),
    ALLOWED_HOSTS=(list, []),
    CSRF_TRUSTED_ORIGINS=(list, []),
    TELEGRAM_TOKEN=(str, ''),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# load config from env
environ.Env.read_env(os.path.join(BASE_DIR, '.env.local'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-a6ll1q%3v&x3jd#fj94ykx)j0g&u+-k2bemn)6p#_b5f^ovb%x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")

# SECURITY WARNING: only use this behind a trusted reverse proxy!
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition
INSTALLED_APPS = [
    'location',
    'app_telegram',
    'app_web',
    'app_api',
    'proto',
    'warning',

    'fontawesomefree',
    'django_tables2',
    'django_celery_results',
    'python_telegram_bot_django_persistence',
    'sitetree',
    'bootstrap5',
    'crispy_forms',
    'crispy_bootstrap5',
    'webpack_loader',
    'rest_framework',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'cwa_venue_notifier.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # default
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # additional
                'django.template.context_processors.i18n',
                'django.template.context_processors.csrf',
                # custom
                'app_web.context_processors.global_vars',
            ],
        },
    },
]

WSGI_APPLICATION = 'cwa_venue_notifier.wsgi.application'


DATA_DIR = os.path.join(BASE_DIR, "data")
PACKAGES_DIR = os.path.join(DATA_DIR, "packages")

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': env.db()
}

# Cache
# https://docs.djangoproject.com/en/4.0/ref/settings/#caches

CACHES = {
    'default': env.cache(backend="django.core.cache.backends.redis.RedisCache")
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'de-de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Crispy forms config
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"

# use sitetree without database
SITETREE_DYNAMIC_ONLY = True

# Theming -> don't load Bootstrap from external sources (CDNs)
BOOTSTRAP5 = {
    # "css_url": {"href": "https://cdn.jsdelivr.net/npm/bootstrap-dark-5@1.1.3/dist/css/bootstrap-dark.min.css"},
}

DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap4.html"

WEBPACK_LOADER = {
  'DEFAULT': {
    'CACHE': not DEBUG,
    'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    'POLL_INTERVAL': 0.1,
    'IGNORE': [r'.+\.hot-update.js', r'.+\.map'],
  }
}


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_SERIALIZER = "pickle"
CELERY_RESULT_SERIALIZER = "pickle"
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_RESULT_BACKEND = env.str("CELERY_RESULT_URL")
CELERY_CACHE_BACKEND = env.str("CELERY_CACHE_URL")
CELERY_BROKER_URL = env.str("BROKER_URL")
CELERY_BEAT_SCHEDULE = {
    "download_packages": {
        "task": "warning.tasks.download_packages",
        "schedule": crontab(hour="*", minute="*/10"),  # run every 10 minutes
    },
}


CWA_BASE_URL = "https://svc90.main.px.t-online.de"
CWA_REGIONS = ['DE']
CWA_MAC_KEY = bytes.fromhex("4357412d4d41432d4b4559")
CWA_ENCRYPTION_KEY = bytes.fromhex("4357412d454e4352595054494f4e2d4b4559")

TELEGRAM_TOKEN = env.str("TELEGRAM_TOKEN")

GLOBAL_IMPRINT_URL = env.str("GLOBAL_IMPRINT_URL")
GLOBAL_PRIVACY_URL = env.str("GLOBAL_PRIVACY_URL")

# Disable CSRF for API
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
    ]
}
