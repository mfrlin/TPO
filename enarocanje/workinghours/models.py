from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext

from enarocanje.accountext.models import ServiceProvider

DAYS_OF_WEEK = (
	('1', _('Monday')),
	('2', _('Tuesday')),
	('3', _('Wednesday')),
	('4', _('Thursday')),
	('5', _('Friday')),
	('6', _('Saturday')),
	('7', _('Sunday')),
)
DAYS_OF_WEEK_DICT = dict(DAYS_OF_WEEK)

class WorkingHours(models.Model):
	service_provider = models.ForeignKey(ServiceProvider, related_name='working_hours')
	time_from = models.TimeField(_('time from'))
	time_to = models.TimeField(_('time to'))
	week_days = models.CommaSeparatedIntegerField(_('week days'), max_length=13)

	def week_days_list(self):
		return self.week_days.split(',')

	def week_days_long(self):
		return u', '.join(ugettext(DAYS_OF_WEEK_DICT[i]) for i in self.week_days_list())

	@classmethod
	def get_for_day(cls, service_provider, day_of_week):
		"""Get working hours for a specific day_of_week (datetime.weekday())"""
		for wh in cls.objects.filter(service_provider=service_provider):
			if str(day_of_week + 1) in wh.week_days_list():
				return wh

	class Meta:
		ordering = ['week_days', 'time_from', 'time_to']

class WorkingHoursBreak(models.Model):
	working_hours = models.ForeignKey(WorkingHours, related_name='breaks')
	time_from = models.TimeField(_('time from'))
	time_to = models.TimeField(_('time to'))

	class Meta:
		ordering = ['time_from', 'time_to']

class Absence(models.Model):
	service_provider = models.ForeignKey(ServiceProvider)
	date_from = models.DateField(_('date from'))
	date_to = models.DateField(_('date to'))

	def days(self):
		return (self.date_to - self.date_from).days + 1

	@classmethod
	def is_absent_on(cls, service_provider, date):
		return cls.objects.filter(service_provider=service_provider, date_from__gte=date, date_to__lte=date).exists()

	class Meta:
		ordering = ['date_from', 'date_to']
