from django import forms
from .models import Customer

from enarocanje.common.widgets import BootstrapDateInput


class CustomerForm(forms.ModelForm):
    last_reservation = forms.DateField(required=True, widget=BootstrapDateInput)

    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'last_reservation']