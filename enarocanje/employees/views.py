from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
import datetime

from enarocanje.accountext.decorators import for_service_providers
from enarocanje.employees.models import Employee
from enarocanje.employees.forms import EmployeeForm, EmployeeServicesForm
from enarocanje.service.models import Service
from enarocanje.workinghours.models import EmployeeWorkingHours
from enarocanje.workinghours.forms import EmployeeWorkingHoursForm


@for_service_providers
def myemployees(request):
    #sp = request.user.service_provider
    employees = Employee.objects.filter(employer=request.user.service_provider)
    return render_to_response('employees/myemployees.html', locals(), context_instance=RequestContext(request))


@for_service_providers
def add(request):
    if request.method == 'POST':
        # set current user as employer implicitly
        form = EmployeeForm(request.POST)
        form_valid = form.is_valid()
        if form_valid:
            employee = form.save(commit=False)
            employee.employer = request.user.service_provider
            employee.save()
            # adding default working hours, ugly fix
            h = EmployeeWorkingHours()
            h.employee = employee
            h.time_from = datetime.time(8)
            h.time_to = datetime.time(16)
            h.week_days = "1,2,3,4,5"
            h.save()
            return HttpResponseRedirect(reverse(myemployees))
    else:
        form = EmployeeForm()
        # render form - new (get request) or invalid with error messages (post request)
    return render_to_response('employees/add.html', locals(), context_instance=RequestContext(request))


@for_service_providers
def edit(request, id):
    provider = request.user.service_provider
    employee = get_object_or_404(Employee, employer=request.user.service_provider, id=id)
    hours = EmployeeWorkingHours.objects.get(employee=employee)
    services = Service.objects.filter(service_provider=provider, employees__in=[employee.id])

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        form_w = EmployeeWorkingHoursForm(request.POST, instance=hours, employee=employee)
        form_s = EmployeeServicesForm(request.POST, service_provider=provider, employee=employee, data=services)
        form_valid = form.is_valid()
        form_w_valid = form_w.is_valid()
        form_s_valid = form_s.is_valid()
        if form_valid and form_w_valid and form_s_valid:
            form.save()
            form_w.save()
            form_s.save()
            return HttpResponseRedirect(reverse(myemployees))
    else:
        form = EmployeeForm(instance=employee)
        form_w = EmployeeWorkingHoursForm(instance=hours, employee=employee)
        form_s = EmployeeServicesForm(service_provider=provider, employee=employee, data=services)
    return render_to_response('employees/edit.html', locals(), context_instance=RequestContext(request))


@for_service_providers
def manage(request):
    if request.method == 'POST':
        employee = get_object_or_404(Employee, employer=request.user.service_provider,
                                     id=request.POST.get('service'))
        if request.POST.get('action') == 'delete':
            employee.delete()
    return HttpResponseRedirect(reverse(myemployees))

