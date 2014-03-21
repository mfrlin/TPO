from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def distance(service_provider, location):
	return u'%.1fkm' % (service_provider.distance(location['lat'], location['lng']))

@register.filter
def logowh(service_provider, wh):
	max_width, max_height = map(int, wh.split(','))
	if service_provider.logo:
		width, height = service_provider.logo_width, service_provider.logo_height
	else:
		width, height = 225, 225  # default.png
	if width > max_width:
		height *= float(max_width) / width
		width = max_width
	if height > max_height:
		width *= float(max_height) / height
		height = max_height
	return mark_safe('width="%d" height="%d"' % (width, height))
