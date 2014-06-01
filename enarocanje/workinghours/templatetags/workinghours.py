from django import template
from django.utils.safestring import mark_safe

from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

