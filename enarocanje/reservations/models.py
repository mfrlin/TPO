import datetime

import celery
from oauth2client.django_orm import CredentialsField
from south.modelsinspector import add_introspection_rules

import pytz
from django.utils import timezone as tz
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.translation import ugettext_lazy as _

from tasks import send_reminder

from enarocanje.accountext.models import User, ServiceProvider
from enarocanje.customers.models import Customer
from enarocanje.employees.models import Employee

add_introspection_rules([], ['^oauth2client\.django_orm\.CredentialsField'])


class Reservation(models.Model):
    """Reservation model - who made a reservation and when"""
    user = models.ForeignKey(User, null=True)  # null for gcal imported reservations
    service = models.ForeignKey('service.Service', null=True, on_delete=models.SET_NULL,
                                related_name='service')  # service can be deleted
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

    # employee
    employee = models.ForeignKey(Employee, null=True)

    show_up = models.NullBooleanField(null=True)

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
    task_id = models.CharField(max_length=256, blank=True, null=True)

    def __unicode__(self):
        return str(self.date) + " User: " + str(self.user) + " Service: " + str(self.service) + " at: " + str(self.time)

    def confirm_reservation(self):
        self.is_confirmed = True
        self.save()

    def deny_reservation(self):
        self.is_deny = True
        self.save()

    def short_desc(self):
        """Default short description visible on reservation button"""
        return str(self.id)

    def active_during(self, time):
        start = datetime.datetime.combine(self.date, self.time)
        end = start + datetime.timedelta(minutes=self.service_duration)
        return time_in_range(start, end, time)

    class Meta:
        unique_together = ('service_provider', 'gcalid')


def customer_handler(sender, instance, created, **kwargs):
    date = datetime.datetime.combine(instance.date, instance.time)
    c = None
    if instance.user:
        c = Customer.objects.filter(user_id=instance.user.id)
    if not c:
        c = Customer.objects.filter(service_id=instance.service_provider.id, email=instance.user_email)
    if not c:
        c_obj = Customer(service_id=instance.service_provider.id, email=instance.user_email)
        c_obj.provider = instance.service_provider
        c_obj.email = instance.user_email
        c_obj.name = instance.user_fullname
        c_obj.phone = instance.user_phone
        c = [c_obj]

    c = c[0]

    if instance.user and not c.user:
        c.user = instance.user

    if created:
        c.last_reservation = date
        c.num_reservations += 1

    c.save()


post_save.connect(customer_handler, sender=Reservation)


def reservation_handler(sender, instance, **kwargs):
    #return

    dt = datetime.datetime.combine(instance.date, instance.time)
    reminder = False
    try:
        obj = Reservation.objects.get(pk=instance.pk)
        if datetime.datetime.combine(obj.date, obj.time) != dt:
            reminder = True
    except Reservation.DoesNotExist:
        obj = instance
        reminder = True

    if reminder:
        # look to see if we have a task_id for this task already.
        if obj.task_id:
            # If we do, lets get rid of this scheduled task
            celery.task.control.revoke(obj.task_id)

        time_zone = tz.get_current_timezone()
        diff = tz.make_aware(dt, time_zone) - tz.now()

        if diff > datetime.timedelta(days=2):
            diff /= 2
        else:
            diff = datetime.timedelta(days=1)

        result = send_reminder.apply_async(eta=dt - diff, kwargs={'reservation': instance})
        instance.task_id = result.task_id


pre_save.connect(reservation_handler, sender=Reservation)


class GCal(models.Model):
    id = models.ForeignKey(ServiceProvider, primary_key=True)
    credential = CredentialsField()


def time_in_range(start, end, x):
    if start <= end:
        return start <= x < end
    else:
        return start <= x or x < end
