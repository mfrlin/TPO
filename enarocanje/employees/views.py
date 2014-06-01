from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.functional import curry
import datetime

from enarocanje.accountext.decorators import for_service_providers
from enarocanje.employees.models import Employee
from enarocanje.employees.forms import EmployeeForm, EmployeeServicesForm
from enarocanje.service.models import Service
from enarocanje.workinghours.models import EmployeeWorkingHours, WorkingHours
from enarocanje.workinghours.forms import EmployeeWorkingHoursForm, EmployeeWorkingHoursFormSet



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
           
            for wh in WorkingHours.objects.filter(service_provider=request.user.service_provider.id):
                h = EmployeeWorkingHours()
                h.employee = employee
                h.time_from = wh.time_from
                h.time_to = wh.time_to
                h.week_days = wh.week_days
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
    hours = EmployeeWorkingHours.objects.filter(employee=employee)
    services = Service.objects.filter(service_provider=provider, employees__in=[employee.id])
    if request.method == 'POST':
        if request.POST.get('action') == 'delete':
            EmployeeWorkingHours.objects.get(id=request.POST.get('workinghours')).delete()
            return HttpResponseRedirect('/myemployees/edit/'+id)
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        qs = EmployeeWorkingHours.objects.filter(employee=employee)
        EmployeeWorkingHoursFormSet.form = staticmethod(curry(EmployeeWorkingHoursForm, employee=employee))
        forms = EmployeeWorkingHoursFormSet(request.POST)
        form_s = EmployeeServicesForm(request.POST, service_provider=provider, employee=employee, data=services)
        form_valid = form.is_valid()
        form_s_valid = form_s.is_valid()
        forms_valid = True
        for f in forms:
            if not f.is_valid():
                forms_valid = False
        if form_valid and form_s_valid and forms_valid:
            form.save()
            for f in forms:
                f.save()
            form_s.save()
            return HttpResponseRedirect(reverse(myemployees))
    else:
        form = EmployeeForm(instance=employee)
        qs = EmployeeWorkingHours.objects.filter(employee=employee)
        EmployeeWorkingHoursFormSet.form = staticmethod(curry(EmployeeWorkingHoursForm, employee=employee))
        forms = EmployeeWorkingHoursFormSet(queryset=qs)
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

