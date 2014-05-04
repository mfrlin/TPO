from settings import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/var/django/enarocanje/enarocanje.db',
        'USER': '',
    }
}
