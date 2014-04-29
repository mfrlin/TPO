from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse

from enarocanje.accountext.decorators import for_service_providers
from enarocanje.employees.models import Employee
from enarocanje.employees.forms import EmployeeForm
from enarocanje.service.models import Service


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
            return HttpResponseRedirect(reverse(myemployees))
    else:
        form = EmployeeForm()
        # render form - new (get request) or invalid with error messages (post request)
    return render_to_response('employees/add.html', locals(), context_instance=RequestContext(request))


@for_service_providers
def edit(request, id):
    employee = get_object_or_404(Employee, employer=request.user.service_provider, id=id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        form_valid = form.is_valid()
        if form_valid:
            form.save()
            return HttpResponseRedirect(reverse(myemployees))
    else:
        form = EmployeeForm(instance=employee)
    return render_to_response('employees/edit.html', locals(), context_instance=RequestContext(request))


@for_service_providers
def manage(request):
    if request.method == 'POST':
        employee = get_object_or_404(Employee, employer=request.user.service_provider,
                                     id=request.POST.get('service'))
        if request.POST.get('action') == 'delete':
            employee.delete()
    return HttpResponseRedirect(reverse(myemployees))

