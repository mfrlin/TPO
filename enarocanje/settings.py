# Django settings for enarocanje project.

import os.path

DEBUG = True
TEMPLATE_DEBUG = True
SOCIAL_LOGIN = False

ROOT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')

BASE_URL = 'http://localhost:80'

ADMINS = ()

MANAGERS = ()

DATABASES = {
'default': {
'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
'NAME': 'enarocanje.db', # Or path to database file if using sqlite3.
'USER': '', # Not used with sqlite3.
'PASSWORD': '', # Not used with sqlite3.
'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
'PORT': '', # Set to empty string for default. Not used with sqlite3.
}
}

DATABASE_SUPPORTS_TRIGONOMETRIC_FUNCTIONS = False

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Ljubljana'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

LOCALE_PATHS = (os.path.join(ROOT_DIR, 'locale'),)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(ROOT_DIR, 'storage/media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(ROOT_DIR, 'storage/static/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
os.path.join(ROOT_DIR, 'static/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
'django.contrib.staticfiles.finders.FileSystemFinder',
'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
#todo set your secret_key
SECRET_KEY = 'c00d$d*ps1sw)4)2e9xbim7_86afat$()=oz-*q!^v#^txdee_'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
'django.template.loaders.filesystem.Loader',
'django.template.loaders.app_directories.Loader',
'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
'django.core.context_processors.request',
'django.contrib.auth.context_processors.auth',
'django.contrib.messages.context_processors.messages',
'allauth.account.context_processors.account',
'allauth.socialaccount.context_processors.socialaccount',
)

MIDDLEWARE_CLASSES = (
'django.middleware.common.CommonMiddleware',
'django.contrib.sessions.middleware.SessionMiddleware',
'django.middleware.csrf.CsrfViewMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'django.middleware.locale.LocaleMiddleware',
'django.contrib.messages.middleware.MessageMiddleware',
'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
'django.contrib.auth.backends.ModelBackend',
'allauth.account.auth_backends.AuthenticationBackend',
)

ROOT_URLCONF = 'enarocanje.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'enarocanje.wsgi.application'

TEMPLATE_DIRS = (
os.path.join(ROOT_DIR, 'templates/'),
)

INSTALLED_APPS = (
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sites',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
'django.contrib.admin',
'django.contrib.admindocs',
'allauth',
'allauth.account',
'allauth.socialaccount',
'bootstrap_toolkit',
'south',
'enarocanje.accountext',
'enarocanje.service',
'enarocanje.workinghours',
'enarocanje.reservations',
'enarocanje.coupon',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
'version': 1,
'disable_existing_loggers': False,
'filters': {
'require_debug_false': {
'()': 'django.utils.log.RequireDebugFalse'
}
},
'handlers': {
'mail_admins': {
'level': 'ERROR',
'filters': ['require_debug_false'],
'class': 'django.utils.log.AdminEmailHandler'
}
},
'loggers': {
'django.request': {
'handlers': ['mail_admins'],
'level': 'ERROR',
'propagate': True,
},
}
}

# AllAuth
AUTH_USER_MODEL = 'accountext.User'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'  # 'mandatory'
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[enarocanje] '
ACCOUNT_SIGNUP_FORM_CLASS = 'enarocanje.accountext.forms.SignupForm'
ACCOUNT_USER_DISPLAY = lambda user: user.get_full_name()
ACCOUNT_USERNAME_REQUIRED = False
SOCIALACCOUNT_AUTO_SIGNUP = False

# Google API. todo enter your info.
GOOGLE_CLIENT_ID = ''
GOOGLE_CLIENT_SECRET = ''
GOOGLE_API_KEY = ''

DEFAULT_FROM_EMAIL = 'info@eorderservice.com'

try:
    from local_settings import *
except ImportError:
    pass

if SOCIAL_LOGIN:
    INSTALLED_APPS += (
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    )
