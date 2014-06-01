from django.utils.translation import ugettext_lazy as _

from django import forms
from .models import Customer

from enarocanje.common.widgets import BootstrapDateInput


class CustomerForm(forms.ModelForm):
    last_reservation = forms.DateField(required=False, widget=BootstrapDateInput)

    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'last_reservation']
        
class ExportListForm(forms.Form):
    selected_list_id = forms.ChoiceField(label=_('Select list'))
