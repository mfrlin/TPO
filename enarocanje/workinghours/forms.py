from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CheckboxSelectMultiple
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _, ugettext

from enarocanje.common.timeutils import is_overlapping
from enarocanje.common.widgets import CSIMultipleChoiceField, BootstrapDateInput, BootstrapTimeInput
from models import WorkingHours, WorkingHoursBreak, Absence, DAYS_OF_WEEK, DAYS_OF_WEEK_DICT

class WorkingHoursForm(ModelForm):
	time_from = forms.TimeField(widget=BootstrapTimeInput(), label=_('Time from'))
	time_to = forms.TimeField(widget=BootstrapTimeInput(), label=_('Time to'))
	week_days = CSIMultipleChoiceField(widget=CheckboxSelectMultiple(), choices=DAYS_OF_WEEK, label='')

	def clean_time_to(self):
		data = self.cleaned_data['time_to']
		if not self.cleaned_data.get('time_from'):
			return data
		if data <= self.cleaned_data['time_from']:
			raise ValidationError(_('Working hours can\'t end before they start.'))
		return data

	def clean_week_days(self):
		data = self.cleaned_data['week_days']
		overlap = set()
		for wh in self.provider.working_hours.all():
			if wh.id != self.instance.id:
				for day in data.split(','):
					if day in wh.week_days_list():
						overlap.add(day)
		if overlap:
			raise ValidationError(_('Working hours are already defined for some of these days (%s).') % u', '.join(ugettext(DAYS_OF_WEEK_DICT[i]) for i in sorted(overlap)))
		return data

	class Meta:
		model = WorkingHours
		exclude = ('service_provider',)

	def __init__(self, *args, **kwargs):
		self.provider = kwargs.pop('provider')
		super(WorkingHoursForm, self).__init__(*args, **kwargs)

class WorkingHoursBreakForm(ModelForm):
	time_from = forms.TimeField(widget=BootstrapTimeInput(), label=_('Time from'))
	time_to = forms.TimeField(widget=BootstrapTimeInput(), label=_('Time to'))

	def clean_time_from(self):
		data = self.cleaned_data['time_from']
		if self.wh_time_from and data <= self.wh_time_from:
			raise ValidationError(_('Breaks must be within working hours.'))
		return data

	def clean_time_to(self):
		data = self.cleaned_data['time_to']
		if self.wh_time_to and data >= self.wh_time_to:
			raise ValidationError(_('Breaks must be within working hours.'))
		if not self.cleaned_data.get('time_from'):
			return data
		if data <= self.cleaned_data['time_from']:
			raise ValidationError(_('Break can\'t end before it starts.'))
		return data

	class Meta:
		model = WorkingHoursBreak

class WorkingHoursBaseFormSet(BaseInlineFormSet):

	def clean(self):
		intervals = []
		for form in self.forms:
			time_from = form.cleaned_data.get('time_from')
			time_to = form.cleaned_data.get('time_to')
			if time_from and time_to:
				for time_from2, time_to2 in intervals:
					if is_overlapping(time_from, time_to, time_from2, time_to2):
						raise ValidationError(_('Breaks can\'t overlap.'))
				intervals.append((time_from, time_to))

WorkingHoursFormSet = inlineformset_factory(WorkingHours, WorkingHoursBreak, form=WorkingHoursBreakForm, formset=WorkingHoursBaseFormSet, extra=1)

class AbsenceForm(ModelForm):
	date_from = forms.DateField(required=True, widget=BootstrapDateInput(), label=_('Date/Date from'))
	date_to = forms.DateField(required=False, widget=BootstrapDateInput(), label=_('Date to'))

	def clean_date_to(self):
		data = self.cleaned_data['date_to']
		if not self.cleaned_data.get('date_from'):
			return data
		if not data:
			return self.cleaned_data['date_from']
		if data < self.cleaned_data['date_from']:
			raise ValidationError(_('Absence can\'t end before it starts.'))
		return data

	class Meta:
		model = Absence
		exclude = ('service_provider',)

	def __init__(self, *args, **kwargs):
		super(AbsenceForm, self).__init__(*args, **kwargs)
		if self.initial.get('date_from') == self.initial.get('date_to'):
			self.initial['date_to'] = None
