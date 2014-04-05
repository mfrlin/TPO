from math import acos, sin, cos, radians
import datetime

import pytz
import requests

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
# from enarocanje.service.views import service_comments


class Category(models.Model):
    name = models.CharField(_('name'), max_length=100)

    def __unicode__(self):
        return self.name


class ServiceProvider(models.Model):
    name = models.CharField(_('name'), max_length=100)
    street = models.CharField(_('street'), max_length=100, null=True, blank=True)
    zipcode = models.CharField(_('zipcode'), max_length=8, null=True, blank=True)
    city = models.CharField(_('city'), max_length=50, null=True, blank=True)
    country = models.CharField(_('country'), max_length=50, null=True, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True, verbose_name=_('Category'))
    timezone = models.CharField(_('timezone'), choices=((x, x,) for x in pytz.common_timezones), default='UTC',
                                max_length=30)

    logo = models.ImageField(upload_to='logos', width_field='logo_width', height_field='logo_height', null=True,
                             blank=True)
    logo_width = models.PositiveIntegerField(null=True)
    logo_height = models.PositiveIntegerField(null=True)

    subscription_end_date = models.DateTimeField(
        default=datetime.datetime.now() + datetime.timedelta(days=30, hours=0, minutes=0, seconds=0))
    subscription_mail_sent = models.BooleanField()

    reservation_confirmation_needed = models.BooleanField()

    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

    gcal_id = models.CharField(max_length=128, null=True)
    gcal_updated = models.DateTimeField(null=True)

    DISTANCE_FORMULA = 'ifnull(acos(sin(radians(%(lat)s)) * sin(radians(accountext_serviceprovider.lat)) + cos(radians(%(lat)s)) * cos(radians(accountext_serviceprovider.lat)) * cos(radians(%(lng)s) - radians(accountext_serviceprovider.lng))) * 6378, 1000000000)'

    def has_location(self):
        return self.lat is not None and self.lng is not None

    def distance(self, lat, lng):
        return acos(sin(radians(lat)) * sin(radians(self.lat)) + cos(radians(lat)) * cos(radians(self.lat)) * cos(
            radians(lng) - radians(self.lng))) * 6378

    def full_address_lines(self):
        return [f for f in (self.street, ' '.join(sf for sf in (self.zipcode, self.city) if sf), self.country) if f]

    def full_address(self):
        return u', '.join(self.full_address_lines())

    def logo_url(self):
        if self.logo:
            return self.logo.url
        return settings.STATIC_URL + 'img/default.png'

    def logo_absolute_url(self):
        return settings.BASE_URL + self.logo_url()

    def get_timezone(self):
        return pytz.timezone(self.timezone)

    def save(self, *args, **kwargs):
        address = self.full_address()
        if address:
            r = requests.get('http://maps.googleapis.com/maps/api/geocode/json',
                             params={'address': address, 'sensor': 'false'})
            results = r.json().get('results') or [{}]
            location = results[0].get('geometry', {}).get('location', {})
            self.lat, self.lng = location.get('lat'), location.get('lng')
        else:
            self.lat, self.lng = None, None
        super(ServiceProvider, self).save(*args, **kwargs)


class User(AbstractUser):
    NOTIFICATION_TYPE_SMS = 0
    NOTIFICATION_TYPE_EMAIL = 1
    NOTIFICATION_TYPES_CHOICES = (
        (NOTIFICATION_TYPE_SMS, _("SMS")),
        (NOTIFICATION_TYPE_EMAIL, _("Email")),
    )
    phone = models.CharField(_('phone number'), max_length=100)
    language = models.CharField(_('language'), max_length=5, choices=settings.LANGUAGES, default='en')
    service_provider = models.OneToOneField(ServiceProvider, null=True)
    referral = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    notification_type = models.SmallIntegerField(_('notification type'),
                                                 choices=NOTIFICATION_TYPES_CHOICES, default=NOTIFICATION_TYPE_EMAIL)

    def has_service_provider(self):
        return bool(self.service_provider_id)

    def referral_url(self):
        return '%s%s?referral=%d' % (settings.BASE_URL, reverse('account_signup'), self.id)


class ServiceProviderImage(models.Model):
    image = models.ImageField(upload_to='images', width_field='image_width', height_field='image_height', null=False,
                              blank=False)
    image_width = models.PositiveIntegerField(null=True)
    image_height = models.PositiveIntegerField(null=True)
    #delete_image = models.BooleanField()
    delete_image = models.BooleanField(default=False)  # temporary fix
    service_provider = models.ForeignKey(ServiceProvider, null=False)
