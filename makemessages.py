#!/usr/bin/python
import distutils.dir_util
import os

import allauth

from django.core.management import execute_from_command_line

# Update allauth
os.system('sudo pip install --upgrade django-allauth')

# Copy allauth source
distutils.dir_util.copy_tree(allauth.__path__[0], 'allauth')

# Run manage.py makemessages
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "enarocanje.settings")
execute_from_command_line(['manage.py', 'makemessages', '--all'])

# Remove allauth source
distutils.dir_util.remove_tree('allauth')
