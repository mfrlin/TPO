from bootstrap_toolkit.widgets import add_to_css_class

from django import forms
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe

class CSIMultipleChoiceField(forms.MultipleChoiceField):

	"""Modified MultipleChoiceField for CommaSeparatedIntegerField"""

	def to_python(self, value):
		return ','.join(value)

	def validate(self, value):
		if value:
			value = value.split(',')
		super(CSIMultipleChoiceField, self).validate(value)

def javascript_date_format(python_date_format):
	format = python_date_format.replace(r'%Y', 'yyyy')
	format = format.replace(r'%m', 'MM')
	format = format.replace(r'%d', 'dd')
	if '%' in format:
		format = ''
	if not format:
		format = 'yyyy-MM-dd'
	return format

def javascript_time_format(python_time_format):
	format = python_time_format.replace(r'%H', 'hh')
	format = format.replace(r'%M', 'mm')
	format = format.replace(r'%S', 'ss')
	if '%' in format:
		format = ''
	if not format:
		format = 'hh:mm'
	return format

class BootstrapDateInput(forms.DateInput):

	bootstrap = {
		'append': mark_safe('<i data-time-icon="icon-time" data-date-icon="icon-calendar"></i>'),
		'prepend': None,
	}

	def __init__(self, attrs=None, format=None):
		if not format:
			format = '%Y-%m-%d'
		super(BootstrapDateInput, self).__init__(attrs, format)

	def render(self, name, value, attrs=None):
		if attrs is None:
			attrs = {}
		attrs['class'] = add_to_css_class(attrs.get('class', ''), 'date-field')
		attrs['data-format'] = javascript_date_format(self.format)
		return super(BootstrapDateInput, self).render(name, value, attrs)

class BootstrapTimeInput(forms.TimeInput):

	bootstrap = {
		'append': mark_safe('<i data-time-icon="icon-time" data-date-icon="icon-calendar"></i>'),
		'prepend': None,
	}

	def __init__(self, attrs=None, format=None):
		if not format:
			format = '%H:%M'
		super(BootstrapTimeInput, self).__init__(attrs, format)

	def render(self, name, value, attrs=None):
		if attrs is None:
			attrs = {}
		attrs['class'] = add_to_css_class(attrs.get('class', ''), 'time-field input-small')
		attrs['data-format'] = javascript_time_format(self.format)
		return super(BootstrapTimeInput, self).render(name, value, attrs)

class ClearableImageInput(forms.ClearableFileInput):
	template_with_initial = '%(initial)s<br />%(clear_template)s<br />%(input)s'
	template_with_clear = '%(clear)s <label for="%(clear_checkbox_id)s" style="display: inline">%(clear_checkbox_label)s</label>'
	url_markup_template = '<img src="{0}" width="220" />'

	# NOTE: not required for django 1.5.2+
	def render(self, name, value, attrs=None):
		substitutions = {
			'initial_text': self.initial_text,
			'input_text': self.input_text,
			'clear_template': '',
			'clear_checkbox_label': self.clear_checkbox_label,
		}
		template = '%(input)s'
		substitutions['input'] = super(forms.ClearableFileInput, self).render(name, value, attrs)

		if value and hasattr(value, "url"):
			template = self.template_with_initial
			substitutions['initial'] = format_html(self.url_markup_template, value.url)
			if not self.is_required:
				checkbox_name = self.clear_checkbox_name(name)
				checkbox_id = self.clear_checkbox_id(checkbox_name)
				substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
				substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
				substitutions['clear'] = forms.CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
				substitutions['clear_template'] = self.template_with_clear % substitutions

		return mark_safe(template % substitutions)
