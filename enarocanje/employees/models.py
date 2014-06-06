# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from enarocanje.accountext.models import ServiceProvider


class Employee(models.Model):
    name = models.CharField(_('name'), max_length=100)
    surname = models.CharField(_('surname'), max_length=100)
    phone = models.CharField(_('phone number'), max_length=100)
    employer = models.ForeignKey(ServiceProvider, null=True, verbose_name=_('Employer'))
    img = models.ImageField(upload_to='employee_images', width_field='img_width', height_field='img_height', null=True,
                            blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    img_width = models.PositiveIntegerField(null=True)
    img_height = models.PositiveIntegerField(null=True)

    def img_url(self):
        if self.img:
            return self.img.url
        return settings.STATIC_URL + 'img/default.png'

    def __unicode__(self):
        return "%s %s" % (self.name, self.surname)