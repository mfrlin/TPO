# -*- coding: utf-8 -*-
import base64
import datetime
import pickle
import urllib
import json
import random

from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import send_mass_mail
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from enarocanje.accountext.decorators import for_service_providers
from enarocanje.accountext.models import User
from enarocanje.common.timeutils import datetime_to_url_format
from enarocanje.coupon.models import Coupon
from enarocanje.reservations.gcal import sync
from enarocanje.reservations.models import Reservation
from enarocanje.service.models import Service
from enarocanje.workinghours.models import WorkingHours
from enarocanje.employees.models import Employee
from forms import ReservationForm, NonRegisteredUserForm
from rcalendar import getMinMaxTime
from enarocanje.common.timeutils import is_overlapping
from enarocanje.workinghours.models import EmployeeWorkingHours

# Service reservations


def reservation(request, id):
    service = get_object_or_404(Service, id=id)
    chosen_employee = None
    emp_size = 0
    if not service.is_active():
        raise Http404
    minTime, maxTime = getMinMaxTime(service.service_provider)

    if request.method != 'POST':
        #form = ReservationForm(request, workingHours=None, service=None)
        form = ReservationForm(request, workingHours=None, service=service)
        data = {'service_provider_id': service.service_provider_id, 'service_id': service.id}
        return render_to_response('reservations/reservation.html', locals(), context_instance=RequestContext(request))

    # POST
    step = request.POST.get('step', '1')

    try:
        data = pickle.loads(base64.b64decode(request.POST.get('data')))  # Serializes an object from request
    except:
        raise Http404

    workingHours = WorkingHours.objects.filter(service_provider_id=service.service_provider_id)

    formNonRegisteredUser = NonRegisteredUserForm()

    if step == '1':
        # Service, date, time
        # form = ReservationForm(request.POST, workingHours='gergerre')
        form = ReservationForm(request, request.POST, workingHours=workingHours, service=service)
        if form.is_valid():
            chosen_employee = form.cleaned_data['employees']
            data['date'] = form.cleaned_data['date']
            data['time'] = form.cleaned_data['time']
            data['number'] = form.cleaned_data['number']
            data['employees'] = form.cleaned_data['employees']

            if request.user.is_authenticated():
                data['user_id'] = request.user.id
                data['name'] = request.user.get_full_name()
                data['phone'] = request.user.phone
                data['email'] = request.user.email
                return render_to_response('reservations/confirmation.html', locals(),
                                          context_instance=RequestContext(request))

            return render_to_response('reservations/userinfo.html', locals(), context_instance=RequestContext(request))

        return render_to_response('reservations/reservation.html', locals(), context_instance=RequestContext(request))

    if step == '2':
        # User info
        if data.get('date') is None or data.get('time') is None:
            raise Http404
        formNonRegisteredUser = NonRegisteredUserForm(request.POST)
        if formNonRegisteredUser.is_valid():
            data['name'] = formNonRegisteredUser.cleaned_data['name']
            data['phone'] = formNonRegisteredUser.cleaned_data['phone']
            data['email'] = formNonRegisteredUser.cleaned_data['email']
            return render_to_response('reservations/confirmation.html', locals(),
                                      context_instance=RequestContext(request))

        return render_to_response('reservations/userinfo.html', locals(), context_instance=RequestContext(request))

    if step == '3':
        # Confirmation
        if data.get('date') is None or data.get('time') is None:  # or data.get('user_id') is None:
            raise Http404
        if data.get('user_id') is not None:
            ruser = get_object_or_404(User, id=data.get('user_id'))
        else:
            ruser = None

        sync(service.service_provider)

        # Checking again if form for reservation is valid
        chosen_employee = data.get('employees')
        print data.get('employees')
        emp_id = None
        if chosen_employee is not None and chosen_employee != '':
            emp_id = chosen_employee.id

        form = ReservationForm(request,
                               {'date': data.get('date'), 'time': data.get('time'), 'employees': emp_id},
                               workingHours=workingHours, service=service)

        if form.is_valid():
            form_emp = None
            if chosen_employee != '':
                form_emp = chosen_employee
            reserve = Reservation(user=ruser, service=service, date=data['date'], time=data['time'],
                                  employee=form_emp)
            # Add backup fields
            reserve.user_fullname = data.get('name')
            reserve.user_phone = data.get('phone')
            reserve.user_email = data.get('email')
            reserve.service_provider = service.service_provider
            reserve.service_name = service.name
            reserve.service_duration = service.duration
            reserve.service_price = service.discounted_price()
            if chosen_employee is not None and chosen_employee != '':
                reserve.employee = chosen_employee
            else:
                # if employees assigned to service, randomly choose one who is free
                if service.employees.all().__len__() > 0:
                    today_r = Reservation.objects.filter(employee__in=service.employees.all(), date=reserve.date)
                    # find free employees
                    reserveDt = datetime.datetime.combine(reserve.date, reserve.time)
                    free_emp = list(service.employees.all())
                    for r in today_r:
                        rDt = datetime.datetime.combine(r.date, r.time)
                        if is_overlapping(reserveDt,
                                          reserveDt + datetime.timedelta(minutes=reserve.service_duration),
                                          rDt, rDt + datetime.timedelta(minutes=reserve.service_duration)):
                            free_emp.remove(r.employee)
                    # choose random employee
                    random_employee = free_emp[random.randint(1, len(free_emp)-1)]
                    reserve.employee = random_employee

            # Save
            reserve.save()
                # saving coupon is_valid
            coupons = Coupon.objects.filter(service=service.id)
            coupon_is_used = False
            for coup in coupons:
                if data['number'] == coup.number:
                    coup.is_used = True
                    coup.save()
                    coupon_is_used = True
                    # Validation checking in form

            user_page_link = '%s/u/%s' % (settings.BASE_URL, reserve.service_provider.userpage_link)
            email_to1 = data.get('email')
            email_to2 = service.service_provider.user.email
            if service.service_provider.reservation_confirmation_needed:
                subject = _('Confirmation of service reservation')
                renderedToCustomer = render_to_string('emails/reservation_customer.html',
                                                      {'reservation': reserve, 'link': user_page_link})
                renderedToProvider = render_to_string('emails/reservation_provider.html',
                                                      {'reservation': reserve, 'link': user_page_link})
                message1 = (subject, renderedToCustomer, None, [email_to1])
                message2 = (subject, renderedToProvider, None, [email_to2])
                send_mass_mail((message1, message2), fail_silently=True)
            else:
                subject = _('Confirmation of service reservation')
                renderedToCustomer = render_to_string('emails/reservation_customer.html',
                                                      {'reservation': reserve, 'link': user_page_link})
                #send_mail(subject, renderedToCustomer, email_to2, [email_to1],
                #          fail_silently=False)

            start = datetime.datetime.combine(reserve.date, reserve.time)
            gcal_params = urllib.urlencode({
                'action': 'TEMPLATE',
                'text': reserve.service_name.encode('utf8'),
                'dates': '%s/%s' % (datetime_to_url_format(start),
                                    datetime_to_url_format(
                                        start + datetime.timedelta(minutes=reserve.service_duration))),
                'details': reserve.service.description.encode('utf8'),
                'location': reserve.service_provider.full_address().encode('utf8'),
                'trp': 'true',
                'sprop': 'E-Narocanje',
                'sprop': 'name:%s' % settings.BASE_URL,
            })
            url_service = settings.BASE_URL + reverse('service', args=(service.id,))

            sync(service.service_provider)

            return render_to_response('reservations/done.html', locals(), context_instance=RequestContext(request))

        # Someone else has made a reservation in the meantime
        return render_to_response('reservations/alreadyreserved.html', locals(),
                                  context_instance=RequestContext(request))
    raise Http404


@for_service_providers
def myreservations(request):
    res_confirm = request.user.service_provider.reservation_confirmation_needed
    return render_to_response('reservations/myreservations.html', locals(), context_instance=RequestContext(request))
