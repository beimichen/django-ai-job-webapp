import logging
import socket

from .base import *  # noqa
#from .base import env

local_ip = str(socket.gethostbyname(socket.gethostname()))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = os.environ['ENV_KEY']
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['www.jobassistant.com','localhost', local_ip]  # os.environ['DJANGO_ALLOWED_HOSTS']

# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': 60,
    },
    # 'chatdb': {
    #      'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #      'NAME': os.environ['RDS_CHAT_DB_NAME'],
    #      'USER': os.environ['RDS_CHAT_USERNAME'],
    #      'PASSWORD': os.environ['RDS_CHAT_PASSWORD'],
    #      'HOST': os.environ['RDS_CHAT_HOSTNAME'],
    #      'PORT': os.environ['RDS_CHAT_PORT'],
    #      'ATOMIC_REQUESTS': True,
    #      'CONN_MAX_AGE': 60,
    #  },
}

# CACHES
# ------------------------------------------------------------------------------
# TODO: update according to https://realpython.com/caching-in-django-with-redis/
REDIS_URL = "redis://" + os.environ['REDIS_HOST'] + ':' + os.environ['REDIS_PORT']

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            # Mimicing memcache behavior.
            # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
            'IGNORE_EXCEPTIONS': True,
        }
    }
}
# Cache time to live is 15 minutes.
CACHE_TTL = 60 * 15

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = True  # env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
# TODO: set this to 60 seconds first and then to 518400 once you prove the former works
SECURE_HSTS_SECONDS = 60
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # env.bool('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = True  # env.bool('DJANGO_SECURE_HSTS_PRELOAD', default=True)
# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = True  # env.bool('DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', default=True)

# STORAGES
# ------------------------------------------------------------------------------
# https://django-storages.readthedocs.io/en/latest/#installation
INSTALLED_APPS += ['storages']  # noqa F405
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_QUERYSTRING_AUTH = False
# DO NOT change these unless you know what you're doing.
_AWS_EXPIRY = 60 * 60 * 24 * 7
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#settings
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': f'max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate',
}



# AWS_HEADERS = {
#     'Expires': 'Thu, 16 May 2019 03:45:32 GMT'
# }

CLOUDFRONT_DOMAIN = "d133ose6pbj6kd.cloudfront.net"

CLOUDFRONT_ID = "E10P4O9O2QQ3Q1"

AWS_S3_CUSTOM_DOMAIN = "d133ose6pbj6kd.cloudfront.net"

AWS_S3_SECURE_URLS = True

AWS_IS_GZIPPED = True

# STATIC
# ------------------------

STATICFILES_STORAGE = 'config.settings.storage.StaticToS3Storage' #'config.settings.staging.StaticRootS3Boto3Storage'
STATIC_URL = "https://d133ose6pbj6kd.cloudfront.net/" # f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/static/' # s3-us-west-2.amazonaws.com/jobassistant-static-west2b/static/


# MEDIA
# ------------------------------------------------------------------------------

# region http://stackoverflow.com/questions/10390244/
# Full-fledge class: https://stackoverflow.com/a/18046120/104731
from storages.backends.s3boto3 import S3Boto3Storage  # noqa E402


class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = 'static'


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False

# endregion
DEFAULT_FILE_STORAGE = 'config.settings.production.MediaRootS3Boto3Storage'
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/'

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES[0]['OPTIONS']['loaders'] = [  # noqa F405
    (
        'django.template.loaders.cached.Loader',
        [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]
    ),
]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = os.environ['DJANGO_DEFAULT_FROM_EMAIL']
# DEFAULT_FROM_EMAIL = env(
#     'DJANGO_DEFAULT_FROM_EMAIL',
#     default='JobAssistant <noreply@jobassistant.com>'
# )
# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = os.environ['DJANGO_SERVER_EMAIL']
# SERVER_EMAIL=  env('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)

# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = "JobAssistant"
#EMAIL_SUBJECT_PREFIX = env('DJANGO_EMAIL_SUBJECT_PREFIX', default='[JobAssistant]')


# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL regex.
ADMIN_URL = os.environ['DJANGO_ADMIN_URL'] # TODO: create DJANOG_ADMIN_URL env var

# Anymail (Mailgun)
# ------------------------------------------------------------------------------
# https://anymail.readthedocs.io/en/stable/installation/#installing-anymail
INSTALLED_APPS += ['anymail']  # noqa F405
EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
# https://anymail.readthedocs.io/en/stable/installation/#anymail-settings-reference
ANYMAIL = {
    'MAILGUN_API_KEY': os.environ['MAILGUN_API_KEY'], # TODO: register mailgun and set MAIL_API_KEY env var
    'MAILGUN_SENDER_DOMAIN': os.environ['MAILGUN_DOMAIN'] # TODO: register mailgun and set MAILGUN_DOMAIN env var
}

# Gunicorn
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['gunicorn']  # noqa F405

# django-compressor
# ------------------------------------------------------------------------------
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_ENABLED
COMPRESS_ENABLED = True  # env.bool('COMPRESS_ENABLED', default=True)
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_STORAGE
COMPRESS_STORAGE = 'config.settings.storage.CachedS3BotoStorage'  # 'storages.backends.s3boto3.S3Boto3Storage'

COMPRESS_OFFLINE = False

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter'
]

# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_URL
COMPRESS_URL = STATIC_URL

STATIC_ROOT = str(BASE_DIR('staticfiles'))

COMPRESS_ROOT = STATIC_ROOT

# COMPRESS_OUTPUT_DIR = "CACHE"

COMPRESS_REBUILD_TIMEOUT = 60 * 15

# COMPRESS_MTIME_DELAY = 10

# COMPRESS_OFFLINE_MANIFEST = 'jobassistant_manifest.json'

# WS_DEFAULT_ACL = None

# Collectfast
# ------------------------------------------------------------------------------
# https://github.com/antonagestam/collectfast#installation
INSTALLED_APPS = ['collectfast'] + INSTALLED_APPS  # noqa F405
AWS_PRELOAD_METADATA = True

# raven
# ------------------------------------------------------------------------------
# https://docs.sentry.io/clients/python/integrations/django/
INSTALLED_APPS += ['raven.contrib.django.raven_compat']  # noqa F405
MIDDLEWARE = [
                 'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
                 # # Google Analytics
                 # 'google_analytics.middleware.GoogleAnalyticsMiddleware',
             ] + MIDDLEWARE

# Sentry
# ------------------------------------------------------------------------------
SENTRY_DSN = os.environ['SENTRY_DSN'] # TODO: register sentry and set SENTRY_DSN env var
SENTRY_CLIENT = 'raven.contrib.django.raven_compat.DjangoClient'
#SENTRY_CLIENT = env('DJANGO_SENTRY_CLIENT', default='raven.contrib.django.raven_compat.DjangoClient')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
    },
}

SENTRY_CELERY_LOGLEVEL = logging.INFO
#SENTRY_CELERY_LOGLEVEL = env.int('DJANGO_SENTRY_LOG_LEVEL', logging.INFO)

RAVEN_CONFIG = {
    'dsn': SENTRY_DSN
}

# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ['django_extensions']  # noqa F405

# JOBASSISTANT specific stuff...
# ------------------------------------------------------------------------------


# Celery
# ------------------------------------------------------------------------------
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = REDIS_URL # REDIS_URL set in cache settings above
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = REDIS_URL
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ['json']
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = 'json'
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = 'json'
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERYD_TASK_TIME_LIMIT = 5 * 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-soft-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERYD_TASK_SOFT_TIME_LIMIT = 60
