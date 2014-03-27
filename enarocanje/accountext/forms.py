from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserChangeForm as DefaultUserChangeForm
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from enarocanje.common.widgets import ClearableImageInput
from enarocanje.reservations.gcal import reset_sync, sync
from models import ServiceProvider, ServiceProviderImage


class UserChangeForm(DefaultUserChangeForm):
    phone = forms.CharField(max_length=100, label=_('Phone Number'))


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label=_('First Name'))
    last_name = forms.CharField(max_length=30, label=_('Last Name'))
    phone = forms.CharField(max_length=100, label=_('Phone Number'))
    language = forms.ChoiceField(choices=settings.LANGUAGES, label=_('Language'))

    def save(self, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.language = self.cleaned_data['language']
        user.save()

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('initial', {}).setdefault('language', 'en')
        super(SignupForm, self).__init__(*args, **kwargs)


class ServiceProviderForm(ModelForm):
    logo = forms.ImageField(widget=ClearableImageInput(), required=False)

    class Meta:
        model = ServiceProvider
        exclude = ('lat', 'lng', 'gcal_id', 'gcal_updated', 'logo_width', 'logo_height', 'subscription_end_date',
                   'subscription_mail_sent', 'subscription_end_date')

    def save(self, *args, **kwargs):
        if self.instance and self.instance.timezone != self.old_timezone:
            print 'reset'
            # reset gcal sync on timezone change
            self.instance = reset_sync(self.instance)
            r = super(ServiceProviderForm, self).save(*args, **kwargs)
            sync(r)
            return r
        return super(ServiceProviderForm, self).save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(ServiceProviderForm, self).__init__(*args, **kwargs)
        self.old_timezone = self.instance.timezone


class ServiceProviderImageForm(ModelForm):
    image = forms.ImageField(required=True, label=_('Upload an image'))

    class Meta:
        model = ServiceProviderImage
        exclude = ('image_width', 'image_height', 'service_provider', 'delete_image')
