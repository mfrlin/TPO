from django import template

from banana_py import Bananas_OAuth

register = template.Library()


@register.simple_tag
def banana_auth_real_url():
    return Bananas_OAuth().authorize_url()

@register.filter
def get_range( value ):
    return range(value)
    
