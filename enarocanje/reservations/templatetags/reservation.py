import base64
import pickle

from django import template

register = template.Library()

@register.filter
def encode_data(data):
	return base64.b64encode(pickle.dumps(data))
