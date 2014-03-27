from oauth2client.django_orm import CredentialsField
from south.modelsinspector import add_introspection_rules

from django.db import models
from django.utils.translation import ugettext_lazy as _

from enarocanje.accountext.models import User, ServiceProvider
from enarocanje.service.models import Service

add_introspection_rules([], ['^oauth2client\.django_orm\.CredentialsField'])


class Reservation(models.Model):
    """Reservation model - who made a reservation and when"""
    user = models.ForeignKey(User, null=True)  # null for gcal imported reservations
    service = models.ForeignKey(Service, null=True, on_delete=models.SET_NULL)  # service can be deleted
    date = models.DateField(null=False, blank=False)
    time = models.TimeField(null=False, blank=False)
    gcalid = models.CharField(max_length=255, null=True)
    isfromgcal = models.BooleanField(default=False)
    # Is confirmed from service provider
    is_confirmed = models.BooleanField(default=False)
    is_deny = models.BooleanField(default=False)
    # Backup fields for user
    user_fullname = models.CharField(_('name'), max_length=60, null=True)
    user_phone = models.CharField(_('phone number'), max_length=100, null=True)
    user_email = models.CharField(_('email address'), max_length=100, null=True)

    # Backup fields if the service is changed or deleted
    service_provider = models.ForeignKey(ServiceProvider, related_name='reservations')
    service_name = models.CharField(_('name'), max_length=100)
    service_duration = models.PositiveIntegerField(_('duration'))
    service_price = models.DecimalField(_('price'), max_digits=7, decimal_places=2, null=True, blank=True)

    # Comments email
    emailsent = models.BooleanField(default=False)

    # Timestamps
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)
    gcalimported = models.DateTimeField(null=True)

    def __unicode__(self):
        return str(self.date) + " User: " + str(self.user) + " Service: " + str(self.service)

    def short_desc(self):
        """Default short description visible on reservation button"""
        return str(self.id)

    class Meta:
        unique_together = ('service_provider', 'gcalid')


class GCal(models.Model):
    id = models.ForeignKey(ServiceProvider, primary_key=True)
    credential = CredentialsField()
