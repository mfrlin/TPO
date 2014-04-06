from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserChangeForm as DefaultUserChangeForm

from enarocanje.common.widgets import ClearableImageInput
from models import ServiceProvider, ServiceProviderImage


class MultiImageField(forms.ImageField):
    widget = ClearableImageInput(attrs={'multiple': 'multiple'})

    def to_python(self, data):
    
        ret = []
        for item in data:
            ret.append(super(MultiImageField, self).to_python(item))

        return ret


class CustomImageField(forms.ImageField):
    def to_python(self, data):
        return super(CustomImageField, self).to_python(data[0])