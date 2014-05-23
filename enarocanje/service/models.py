import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

from enarocanje.accountext.models import ServiceProvider, User
from enarocanje.reservations.models import Reservation
from enarocanje.employees.models import Employee


class Category(models.Model):
    name = models.CharField(_('name'), max_length=100)

    show_in_gallery = models.BooleanField(_('Show in gallery'))

    def __unicode__(self):
        return "%s" % self.name


class Service(models.Model):
    MALE = 'm'
    FEMALE = 'f'
    SEX_SERVICE_CHOICES = (
        (MALE, _('Male')),
        (FEMALE, _('Female')),
    )

    service_provider = models.ForeignKey(ServiceProvider, related_name='services')
    name = models.CharField(_('name'), max_length=100)
    duration = models.PositiveIntegerField(_('duration'))
    description = models.TextField(_('description'), null=True, blank=True)
    price = models.DecimalField(_('price'), max_digits=7, decimal_places=2, null=True, blank=True)
    sex = models.CharField(_('sex'), choices=SEX_SERVICE_CHOICES, max_length=1, null=True, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True)
    active_until = models.DateField(_('active until'), null=True, blank=True)
    employees = models.ManyToManyField(Employee, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def duration_with_unit(self):
        return u'%dmin' % self.duration

    def get_discount(self):
        try:
            return self.discounts.get(valid_from__lte=datetime.date.today(), valid_to__gte=datetime.date.today())
        except ObjectDoesNotExist:
            return None

    def discounted_price(self):
        discount = self.get_discount()
        if discount:
            #so 99% and similar discounts don't return too many decimal places
            n = round(self.price - discount.discount * self.price / 100, 2)
            if n % 1 == 0:
                return int(n)
            else:
                return n
        else:
            return self.price

    def price_with_unit(self):
        discount = self.get_discount()
        if discount:
            if self.discounted_price() == 0.00:
                #return u'Free (%s -%d%%)' % (ugettext(_('with')), discount.discount)
                return _("Free")
            else:
                return u'%.02f\u20ac (%s -%d%%)' % (self.discounted_price(), ugettext(_('with')), discount.discount)
        else:
            if not self.price:
                return _("Free")
            else:
                return u'%.02f\u20ac' % self.price

    def is_active(self):
        return self.active_until is None or self.active_until >= datetime.date.today()

    def get_reservations(self):
        return Reservation.objects.filter(service=self)


class Discount(models.Model):
    service = models.ForeignKey(Service, related_name='discounts', verbose_name=_('service'))
    discount = models.PositiveIntegerField(_('discount'))
    valid_from = models.DateField(_('discount valid from'))
    valid_to = models.DateField(_('discount valid to'))

    def discount_with_unit(self):
        return u'%d%%' % self.discount


class Comment(models.Model):
    service = models.ForeignKey(Service, related_name='comments', verbose_name=_('service'))
    author = models.ForeignKey(User, related_name='comments', verbose_name=_('author'))
    body = models.TextField(_('body'))
    created = models.DateTimeField(auto_now_add=True)
