from django.forms import ModelForm, Form, ModelMultipleChoiceField
import django.forms as forms
from enarocanje.accountext.models import ServiceProvider
from enarocanje.service.models import Service

from enarocanje.employees.models import Employee


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        exclude = ('employer', )

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)


class EmployeeServicesForm(Form):
    def __init__(self, *args, **kwargs):
        self.provider = kwargs.pop('service_provider')
        self.employee = kwargs.pop('employee')
        data = kwargs.pop('data')
        self.services = ModelMultipleChoiceField(
            queryset=Service.objects.all().filter(service_provider_id=self.provider.id),
            widget=forms.CheckboxSelectMultiple, initial=data)
        super(EmployeeServicesForm, self).__init__(*args, **kwargs)
        self.fields['services'] = self.services

    def save(self):
        provider_services = Service.objects.all().filter(service_provider_id=self.provider.id)
        services = self.cleaned_data['services']
        s_set = set(provider_services).difference(services)
        for service in provider_services:
            if service not in s_set:
                service.employees.add(self.employee.id)
            elif service in s_set:
                service.employees.remove(self.employee.id)

