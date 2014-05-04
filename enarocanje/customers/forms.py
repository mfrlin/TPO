from django import forms
from .models import Customer

from enarocanje.common.widgets import BootstrapDateTimeInput


class CustomerForm(forms.ModelForm):
    last_reservation = forms.DateTimeField(required=True, widget=BootstrapDateTimeInput())

    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'last_reservation']