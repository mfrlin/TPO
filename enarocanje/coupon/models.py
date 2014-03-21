from django.db import models
from django.utils.translation import ugettext_lazy as _

from enarocanje.accountext.models import ServiceProvider
from enarocanje.service.models import Service

class Coupon(models.Model):
	service_provider = models.ForeignKey(ServiceProvider, related_name='coupons')
	service = models.ForeignKey(Service, related_name='coupons', verbose_name=_('service'))
	number = models.CharField(_('number'), max_length=15)
	valid = models.DateField(_('valid'))
	is_used = models.BooleanField(_('is valid'), default=False)
