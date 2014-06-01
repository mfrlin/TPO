from django.db import models
from django.utils.translation import ugettext_lazy as _
from enarocanje.accountext.models import User, ServiceProvider


class Customer(models.Model):
    user = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=255)
    service = models.ForeignKey(ServiceProvider)
    num_reservations = models.IntegerField(default=0)
    phone = models.CharField(_('phone number'), max_length=100)
    email = models.EmailField(_('email address'))
    last_reservation = models.DateField(null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ("service", "email")


