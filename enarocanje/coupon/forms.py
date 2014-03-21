from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from enarocanje.common.widgets import BootstrapDateInput
from models import Coupon, Service

date_formats = [
	'%Y-%m-%d',              # '2006-10-25'
	'%m/%d/%Y',              # '10/25/2006'
	'%m/%d/%y',              # '10/25/06'
	'%d.%m.%Y',              # '25.10.2006'
	'%d.%m.%y',              # '25.10.06'
]

class CouponForm(ModelForm):

	"""Form for adding and editing coupons"""
	valid = forms.DateField(widget=BootstrapDateInput(), required=True, label=_('Coupon valid until'), input_formats=date_formats)

	class Meta:
		model = Coupon
		# all fields except service_provider (you can only create your own services)
		exclude = ('service_provider',)

	def __init__(self, *args, **kwargs):
		provider = kwargs.pop('provider')
		super(CouponForm, self).__init__(*args, **kwargs)
		self.fields['service'].queryset = provider.services

class CsvForm(forms.Form):
	service = forms.ModelChoiceField(queryset=Service.objects.none(), label=_('Service'))
	file = forms.FileField(label='')

	def __init__(self, *args, **kwargs):
		provider = kwargs.pop('provider')
		super(CsvForm, self).__init__(*args, **kwargs)
		self.fields['service'].queryset = provider.services
