"""
Django settings for nugis project.

All deployment-specific values come from environment variables
(see README.md and .envs/).
"""

import os

import environ

env = environ.Env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = env.bool('DEBUG', default=False)

# SECRET_KEY is mandatory outside of DEBUG. Never commit a real one.
if DEBUG:
    SECRET_KEY = env('SECRET_KEY', default='insecure-local-development-key')
else:
    SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'] if DEBUG else [])
# Backwards compatibility with the old single-host variable.
if env('ALLOWED_HOST', default=None):
    ALLOWED_HOSTS.append(env('ALLOWED_HOST'))

CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'drf_yasg',
    'corsheaders',
]
LOCAL_APPS = [
    'music',
    'users',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# django-debug-toolbar is optional (requirements-dev.txt).
if DEBUG:
    try:
        import debug_toolbar  # noqa: F401
    except ImportError:
        pass
    else:
        INSTALLED_APPS.append('debug_toolbar')
        MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
        INTERNAL_IPS = ['127.0.0.1']

ROOT_URLCONF = 'nugis.urls'

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

WSGI_APPLICATION = 'nugis.wsgi.application'

# Database: DATABASE_URL wins; otherwise the POSTGRES_* variables used by
# docker compose.
if env('DATABASE_URL', default=None):
    DATABASES = {'default': env.db('DATABASE_URL')}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('POSTGRES_DB', default='postgres_db'),
            'USER': env('POSTGRES_USER', default='postgres_role'),
            'PASSWORD': env('POSTGRES_PASSWORD', default=''),
            'HOST': env('POSTGRES_HOST', default='postgres'),
            'PORT': env('POSTGRES_PORT', default='5432'),
        }
    }

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'static')
STATIC_URL = '/static/'
MEDIA_ROOT = env('MEDIA_ROOT', default=os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'media'))
MEDIA_URL = '/media/'
FILE_UPLOAD_PERMISSIONS = 0o644

# Max size of an uploaded track, in bytes.
MAX_TRACK_SIZE = env.int('MAX_TRACK_SIZE', default=10 * 1024 * 1024)

# Security headers when served behind TLS.
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = env.bool('SECURE_COOKIES', default=True)
    CSRF_COOKIE_SECURE = env.bool('SECURE_COOKIES', default=True)
    SECURE_CONTENT_TYPE_NOSNIFF = True

# DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# CORS: the frontend runs on another origin. Audio files also need CORS so
# the Web Audio equalizer can process them.
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])
CORS_ALLOW_ALL_ORIGINS = env.bool('CORS_ALLOW_ALL_ORIGINS', default=DEBUG and not CORS_ALLOWED_ORIGINS)

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        },
    },
}

# Sentry (optional)
SENTRY_DSN = env('SENTRY_DSN', default=None)
if SENTRY_DSN:
    import sentry_sdk

    sentry_sdk.init(dsn=SENTRY_DSN, send_default_pii=False)
