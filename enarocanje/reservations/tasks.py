from __future__ import absolute_import
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _

from celery import shared_task

@shared_task
def send_reminder(reservation):
    body = "Test text"
    to = [reservation.user_email, ]
    frm = "foo@bar.com"
    subject = _("Reservation reminder")
    send_mail(subject, body, frm, to, fail_silently=False)