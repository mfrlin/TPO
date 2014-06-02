from django.utils.translation import ugettext_lazy as _

from django import forms
from .models import Customer
from django.forms import Form


from enarocanje.common.widgets import BootstrapDateInput


class CustomerForm(forms.ModelForm):
    last_reservation = forms.DateField(required=False, widget=BootstrapDateInput)

    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'last_reservation']
        

class CustomerChoiceForm(Form):
    def __init__(self, *args, **kwargs):
        qs = Customer.objects.filter(service=kwargs.pop('provider'))
        print qs
        self.customers = forms.ModelChoiceField(queryset=qs, required=False,
                                                empty_label=_('all'))
        super(CustomerChoiceForm, self).__init__(*args, **kwargs)
        self.fields['customers'] = self.customers


class ExportListForm(forms.Form):
    selected_list_id = forms.ChoiceField(label=_('Select list'))

class ChoiceRowForm(forms.Form):
    selected_list_id = forms.ChoiceField(choices=[(0,_("Name")),(1,_("Email")),(2,_("Phone number"))])

class UploadFileForm(forms.Form):
    delimiter = forms.CharField(max_length=1, initial=',')
    quote = forms.CharField(max_length=1, initial='"')
    file  = forms.FileField(widget=forms.FileInput())