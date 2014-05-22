import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from enarocanje.common.timeutils import is_overlapping
from enarocanje.common.widgets import BootstrapDateInput, BootstrapTimeInput
from enarocanje.coupon.models import Coupon
from enarocanje.reservations.models import Reservation
from enarocanje.workinghours.models import WorkingHours, Absence
from enarocanje.employees.models import Employee


def getDefaultReservationDate():
    return datetime.datetime.now().date()


def getDefaultReservationTime():
    time = datetime.datetime.now().time()
    if time.minute >= 45:
        if time.hour == 23:
            return datetime.time(0)
        return datetime.time(time.hour + 1)
    return datetime.time(time.hour, time.minute // 15 * 15 + 15)


class ReservationForm(forms.Form):
    date = forms.DateField(widget=BootstrapDateInput(), initial=getDefaultReservationDate, label=_('Date'))
    time = forms.TimeField(widget=BootstrapTimeInput(), initial=getDefaultReservationTime, label=_('Time'))
    number = forms.CharField(required=False, label='')

    def clean_number(self):
        data = self.cleaned_data['number']
        coupons = Coupon.objects.filter(service=self.service.id)
        saved_time = self.request.session.get('start_session', None)
        now = datetime.datetime.now()
        if data:
            if saved_time is not None and (saved_time < now and self.request.session.get('count') == 10):
                del self.request.session['count']
                del self.request.session['start_session']
            if 'count' in self.request.session:
                if self.request.session.get('count') == 10:
                    self.request.session['start_session'] = now + datetime.timedelta(days=1)
                    raise ValidationError(
                        _('Sorry, you entered your coupon number wrong 10 times. You can try again in 24h.'))
                else:
                    self.request.session['count'] = self.request.session.get('count', 0) + 1
            else:
                self.request.session['count'] = 1
            for coup in coupons:
                if data == coup.number and (saved_time is None or saved_time <= now):
                    if coup.valid >= now.date():
                        if coup.is_used:
                            raise ValidationError(_('Sorry, this coupon was already used.'))
                        if 'count' and 'start_session' in self.request.session:
                            del self.request.session['count']
                            del self.request.session['start_session']
                        return data
                    raise ValidationError(
                        _('Sorry, you coupon is not valid at this time. Check expiry date of your coupon'))
            raise ValidationError(_('Sorry, your coupon number is not valid. Please try again.'))

    def clean_date(self):
        now = datetime.datetime.now()
        data = self.cleaned_data.get('date')
        if not data:
            return data

        # Check that selected date is not in the past
        if data < now.date():
            raise ValidationError(_('Sorry, you can\'t make reservations for past days.'))

        service_provider = self.service.service_provider

        # Check if it's overlapping with working days (convert date to weekday and check if it's in the week_days list)
        workinghrs = WorkingHours.get_for_day(service_provider, data.weekday())
        if workinghrs is None:
            raise ValidationError(_('Sorry, you can\'t make a reservation on a non working day.'))

        # Check if it's overlapping with absences
        if Absence.is_absent_on(service_provider, data):
            raise ValidationError(_('Sorry, the provider is absent on this day.'))

        return data

    def clean_time(self):
        now = datetime.datetime.now()
        data = self.cleaned_data.get('time')
        if not data or not self.cleaned_data.get('date'):
            return data

        start = datetime.datetime.combine(self.cleaned_data['date'], data)
        end = start + datetime.timedelta(minutes=self.service.duration)

        if start.date() != end.date():
            raise ValidationError(_('Sorry, reservation can\'t span over multiple days.'))

        # Check current time with date
        if start < now:
            raise ValidationError(_('Sorry, you can\'t make a reservation in the past.'))

        service_provider = self.service.service_provider

        # Check working hours
        wrk = WorkingHours.get_for_day(service_provider, start.weekday())
        if start.time() < wrk.time_from:
            raise ValidationError(_('Sorry, the service isn\'t available before ' + str(wrk.time_from)[:-3]))
        elif end.time() > wrk.time_to:
            raise ValidationError(_('Sorry, the service is closed from ' + str(wrk.time_to)[:-3]))

        # Check pauses
        for wrkBr in wrk.breaks.all():
            if is_overlapping(start.time(), end.time(), wrkBr.time_from, wrkBr.time_to):
                raise ValidationError(_('Sorry, the service isn\'t available at specified time.'))

        # Check reservations
        reservations = Reservation.objects.filter(service_provider=service_provider, date=self.cleaned_data.get('date'))
        # if employee is chosen, only check against his reservations
        if self.clean_employees() != '':
            reservations = reservations.filter(employee=self.clean_employees().id)
            slots = 1
        else:
            slots = list(self.service.employees.all()).__len__()

        print slots
        for res in reservations:
            resDt = datetime.datetime.combine(res.date, res.time)
            if is_overlapping(start, end, resDt, resDt + datetime.timedelta(minutes=res.service_duration)):
                slots -= 1
            if slots == 0:
                raise ValidationError(_('Sorry, your reservation is overlapping with another reservation.'))

        print slots

        return data

    def clean_employees(self):
        if 'employees' in self.data:
            if self.data['employees'] != '' and self.data['employees'] is not None:
                return Employee.objects.get(id=self.data['employees'])
        return ''

    def __init__(self, request, *args, **kwargs):
        self.workingHours = kwargs.pop('workingHours')
        self.service = kwargs.pop('service')
        self.request = request
        if self.service.employees.all():
            self.employees = forms.ModelChoiceField(queryset=self.service.employees, required=False,
                                                    empty_label=_('anyone'))
        else:
            self.employees = forms.ModelChoiceField(queryset=Employee.objects.none(), required=False)
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['employees'] = self.employees


class NonRegisteredUserForm(forms.Form):
    name = forms.CharField(max_length=60, label=_('Name'), required=True)
    phone = forms.CharField(max_length=100, label=_('Phone Number'), required=True)
    email = forms.CharField(max_length=30, label=_('Email address'), required=True)


class GCalSettings(forms.Form):
    def __init__(self, *args, **kwargs):
        calendars = kwargs.pop('calendars')
        super(GCalSettings, self).__init__(*args, **kwargs)
        self.fields['calendar'] = forms.ChoiceField(
            widget=forms.RadioSelect(),
            choices=[
                        (None, _('Don\'t sync with Google Calendar')),
                        ('new', _('Create new calendar'))
                    ] +
                    [
                        (calendar['id'], calendar['summary'])
                        for calendar in calendars
                        if calendar['accessRole'] in ('writer', 'owner')
                    ],
            label=''
        )
