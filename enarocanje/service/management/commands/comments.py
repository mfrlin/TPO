import datetime

from django.conf import settings
from django.core.mail import send_mass_mail
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from enarocanje.reservations.models import Reservation

class Command(BaseCommand):

	def handle(self, *args, **options):
		now = datetime.datetime.now()
		messages = []
		for reservation in Reservation.objects.select_for_update().filter(user__isnull=False, service__isnull=False, date__lte=now.date(), emailsent=False).order_by('date', 'time'):
			if now >= datetime.datetime.combine(reservation.date, reservation.time):
				# Activate correct translation language
				translation.activate(reservation.user.language)
				# Render message
				url = settings.BASE_URL + reverse('servicecomments', args=(reservation.service.id,))
				messages.append((_('Review your service reservation'), render_to_string('emails/comment.html', {'reservation': reservation, 'url': url}), None, [reservation.user.email]))
				# Set emailsent
				reservation.emailsent = True
				reservation.save()

		# Send emails
		send_mass_mail(messages, fail_silently=True)
		print len(messages), 'emails sent.'
