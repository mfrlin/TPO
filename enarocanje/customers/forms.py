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

