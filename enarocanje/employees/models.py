# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

from django.db import models
from django.utils.translation import ugettext_lazy as _
from enarocanje.accountext.models import ServiceProvider


class Employee(models.Model):
    name = models.CharField(_('name'), max_length=100)
    surname = models.CharField(_('surname'), max_length=100)
    phone = models.CharField(_('phone number'), max_length=100)
    employer = models.ForeignKey(ServiceProvider, null=True, verbose_name=_('Employer'))


class EmployeeImage(models.Model):
    image = models.ImageField(upload_to='images', width_field='image_width', height_field='image_height', null=False,
                              blank=False)
    image_width = models.PositiveIntegerField(null=True)
    image_height = models.PositiveIntegerField(null=True)
    delete_image = models.BooleanField(default=False)  # originally was without default
    employee = models.ForeignKey(Employee, null=False)
