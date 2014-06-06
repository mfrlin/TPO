from __future__ import absolute_import
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from enarocanje.accountext.models import User

from celery import shared_task


@shared_task
def send_reminder(reservation):
    send_email = reservation.user.notification_type == User.NOTIFICATION_TYPE_EMAIL
    if send_email:
        user_page_link = '%s/u/%s' % (settings.BASE_URL, reservation.service_provider.userpage_link)
        subject = unicode(_("Reservation reminder"))
        body = render_to_string('emails/reminder.html', {'reservation': reservation, 'link': user_page_link})
        to = [reservation.user_email, ]
        frm = settings.DEFAULT_FROM_EMAIL
        send_mail(subject, body, frm, to, fail_silently=False)
    else:
        raise NotImplementedError("Please implement sending SMSes")