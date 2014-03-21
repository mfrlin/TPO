from django.core.management.base import BaseCommand

from enarocanje.accountext.models import ServiceProvider
from enarocanje.reservations.gcal import sync

class Command(BaseCommand):

	def handle(self, *args, **options):
		counter_created = 0
		counter_updated = 0
		counter_imported = 0
		for provider in ServiceProvider.objects.all():
			c, u, i = sync(provider)
			counter_created += c
			counter_updated += u
			counter_imported += i

		self.stdout.write('%d created, %d updated, %d imported' % (counter_created, counter_updated, counter_imported))
