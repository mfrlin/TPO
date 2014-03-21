import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

from enarocanje.accountext.models import ServiceProvider, User

class Category(models.Model):
	name = models.CharField(_('name'), max_length=100)

	def __unicode__(self):
		return "%s" % (self.name)

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
			return self.price - discount.discount * self.price / 100
		else:
			return self.price

	def price_with_unit(self):
		discount = self.get_discount()
		if discount:
			return u'%s\u20ac (%s -%d%%)' % (self.discounted_price(), ugettext(_('with')), discount.discount)
		else:
			return u'%s\u20ac' % self.price

	def is_active(self):
		return self.active_until is None or self.active_until >= datetime.date.today()

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
