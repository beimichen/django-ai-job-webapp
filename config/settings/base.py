"""
Base settings to build other settings files upon.
"""

import environ
import os

BASE_DIR = environ.Path(__file__) - 3  # (jobassistant/config/settings/base.py - 3 = jobassistant/)
APPS_DIR = BASE_DIR.path('jobassistant')

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# APPS_DIR = BASE_DIR.path('jobassistant')


# START OF DOCKER SETTINGS FOR ENV VARS

# env = os.environ

# READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)

#  Use .env when you have docker  #

# if READ_DOT_ENV_FILE:
#     # OS environment variables take precedence over variables from .env
#     env.read_env(str(ROOT_DIR.path('.env')))

# END OF DOCKER SETTINGS FOR ENV VARS

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = 'Australia/Melbourne'
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True


# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

# Database routing for chat app

# DATABASE_ROUTERS = ['jobassistant.chat.router.DatabaseAppsRouter', 'jobassistant.cover_letter_tracking.router.DatabaseAppsRouter']
# DATABASE_APPS_MAPPING = [{'chat': 'chatdb'}, {'cover_letter_tracking': 'chatdb'}]

# Database settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'jobassistantdb',
        'USER': 'postgres',
        'PASSWORD': os.environ.get('DB_PASSWORD', 'change-me'),
        'HOST': '127.0.0.1',
        # 'HOST': 'YOUR_RDS_HOST',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True,
    },
    # 'chatdb': {
    #      'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #      'NAME': 'chatdb',
    #      'USER': 'postgres',
    #      'PASSWORD': os.environ.get('DB_PASSWORD', 'change-me'),
    #      'HOST': '127.0.0.1',
    #      # 'HOST': 'YOUR_RDS_HOST',
    #      'PORT': '5432',
    #      'ATOMIC_REQUESTS': True,
    # },
}

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'jquery',
    'djangoformsetjs',
    # 'django.contrib.humanize', # Handy template tags
    'dal', #  django-auto-complete https://django-autocomplete-light.readthedocs.io/en/master/install.html#install-in-your-project
    'dal_select2',  #  django-auto-complete https://django-autocomplete-light.readthedocs.io/en/master/install.html#install-in-your-project
    'django.contrib.admin',
]
THIRD_PARTY_APPS = [
    'bootstrap4',
    'crispy_forms',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'bootstrap_datepicker_plus',
    'bootstrap_modal_forms',
    'widget_tweaks',
    'smart_selects',
    'phonenumbers',
    'phonenumber_field',
    'extra_views',
    'braces',
    'taggit',
    'taggit_serializer',
    'taggit_selectize',
]
LOCAL_APPS = [
    'jobassistant.users.apps.UsersAppConfig',
    'jobassistant.cover_letter.apps.CoverLetterConfig',
    'jobassistant.cover_letter_tracking.apps.CoverLetterTrackingConfig',
    'jobassistant.chat.apps.ChatConfig',
    'jobassistant.resume.apps.ResumeConfig',
    'jobassistant.dashboard.apps.DashboardConfig',
    'jobassistant.contact.apps.ContactConfig',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'config.urls'
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# REST FRAMEWORK
# ------------------------------------------------------------------------------
# https://www.django-rest-framework.org/
REST_FRAMKEWORK = {
    'DEFAULT_PERMISSION_CLAASES': (
        # 'rest_framework.permissions.AllowAny',
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

# REST_SESSION_LOGIN = False


# CORS ORIGIN SETTINGS
# ------------------------------------------------------------------------------
# https://stackoverflow.com/questions/35760943/how-can-i-enable-cors-on-django-rest-framework

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    'localhost:*',
    'www.jobassistant.com',
    'www.jobassistant.com/*',
)
CORS_ORIGIN_REGEX_WHITELIST = (
    'localhost:*',
    'www.jobassistant.com',
    'www.jobassistant.com/*',
)

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {
    'sites': 'jobassistant.contrib.sites.migrations'
}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = 'users.User'
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = 'users:redirect'
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = 'account_login'

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
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

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(BASE_DIR('staticfiles'))
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(APPS_DIR.path('static')),
]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('media'))
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'jobassistant.dashboard.resume_context_processors.personal_check_complete',
                'jobassistant.dashboard.resume_context_processors.experience_check_complete',
                'jobassistant.dashboard.resume_context_processors.education_check_complete',
                'jobassistant.dashboard.resume_context_processors.reference_check_complete',
            ],
        },
    },
]
# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (
    str(APPS_DIR.path('fixtures')),
)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
# SESSION_COOKIE_HTTPONLY = True
CSRF_USE_SESSIONS = False
CSRF_COOKIE_NAME = 'csrftoken'
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
# CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = 'DENY'

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = 'admin/'
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
    ("""JobAssistant Team""", 'jobassistant@jobassistant.com'),
    ("""Admin""", 'admin@example.com'),
]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# Celery
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['jobassistant.taskapp.celery.CeleryAppConfig']
if USE_TZ:
    # http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-timezone
    CELERY_TIMEZONE = TIME_ZONE
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = 'redis://localhost:6379'
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
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
# django-allauth
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = 'username'
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_ADAPTER = 'jobassistant.users.adapters.AccountAdapter'
# https://django-allauth.readthedocs.io/en/latest/configuration.html
SOCIALACCOUNT_ADAPTER = 'jobassistant.users.adapters.SocialAccountAdapter'

# django-compressor
# ------------------------------------------------------------------------------
# https://django-compressor.readthedocs.io/en/latest/quickstart/#installation
INSTALLED_APPS += ['compressor']
STATICFILES_FINDERS += ['compressor.finders.CompressorFinder']
# COMPRESS_URL = "'https://jobassistant-static-west2b.s3.amazonaws.com/static"

# Taggit Selectize
# ------------------------------------------------------------------------------
# https://github.com/chhantyal/taggit-selectize
TAGGIT_TAGS_FROM_STRING = 'taggit_selectize.utils.parse_tags'
TAGGIT_STRING_FROM_TAGS = 'taggit_selectize.utils.join_tags'

TAGGIT_SELECTIZE = {
    'MINIMUM_QUERY_LENGTH': 2,
    'RECOMMENDATION_LIMIT': 6,
    'CSS_FILENAMES': ("taggit_selectize/css/selectize.django.css",),
    'JS_FILENAMES': ("taggit_selectize/js/selectize.js",),
    'DIACRITICS': True,
    'CREATE': True,
    'PERSIST': True,
    'OPEN_ON_FOCUS': True,
    'HIDE_SELECTED': True,
    'CLOSE_AFTER_SELECT': False,
    'LOAD_THROTTLE': 300,
    'PRELOAD': False,
    'ADD_PRECEDENCE': False,
    'SELECT_ON_TAB': False,
    'REMOVE_BUTTON': False,
    'RESTORE_ON_BACKSPACE': False,
    'DRAG_DROP': False,
    'DELIMITER': ','
}

# BOOTSTRAP 4

BOOTSTRAP4 = {
    'include_jquery': True,
}
