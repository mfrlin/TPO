from __future__ import absolute_import
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

from .models import Reservation

from celery import shared_task


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

@shared_task
def send_reminder(pk):
    reservation = Reservation.objects.get(pk=pk)
    body = "Test text"
    to = [reservation.user_email, 'martin.frlin@gmail.com']
    frm = "foo@bar.com"
    subject = _("Reservation reminder")
    send_mail(subject, body, frm, to, fail_silently=False)