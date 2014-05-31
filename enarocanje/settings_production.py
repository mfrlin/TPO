from settings import *

DEBUG = False

SOCIAL_LOGIN = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/var/django/enarocanje/enarocanje.db',
        'USER': '',
    }
}

BASE_URL = 'http://boc.fri.uni-lj.si'

if SOCIAL_LOGIN:
    INSTALLED_APPS += (
        'allauth.socialaccount.providers.google',
        'allauth.socialaccount.providers.facebook',
    )
