from django.forms import ModelForm, Form, ModelMultipleChoiceField, Textarea, TextInput
from enarocanje.common.widgets import ClearableImageInput
import django.forms as forms
from django.utils.translation import ugettext_lazy as _
from enarocanje.accountext.models import ServiceProvider
from enarocanje.service.models import Service

from enarocanje.employees.models import Employee


class EmployeeForm(ModelForm):
    img = forms.ImageField(widget=ClearableImageInput(), required=False, label=_('Employee image'))
    description = forms.CharField(widget=Textarea(), required=False)

    class Meta:
        model = Employee
        exclude = ('employer', 'img_width', 'img_height')

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)


class EmployeeServicesForm(Form):
    def __init__(self, *args, **kwargs):
        self.provider = kwargs.pop('service_provider')
        self.employee = kwargs.pop('employee')
        data = kwargs.pop('data')
        self.services = ModelMultipleChoiceField(
            queryset=Service.objects.all().filter(service_provider_id=self.provider.id),
            widget=forms.CheckboxSelectMultiple, initial=data, required=False)
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


class EmployeeChoiceForm(Form):
    def __init__(self, *args, **kwargs):
        qs = Employee.objects.filter(employer=kwargs.pop('provider'))
        self.employees = forms.ModelChoiceField(queryset=qs, required=False,
                                                empty_label=_('all'))
        super(EmployeeChoiceForm, self).__init__(*args, **kwargs)
        self.fields['employees'] = self.employees
