from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserChangeForm as DefaultUserChangeForm
from django.forms import ModelForm, BaseForm, Form
from django.forms.formsets import formset_factory

from django.utils.translation import ugettext_lazy as _

from enarocanje.common.widgets import ClearableImageInput
from enarocanje.reservations.gcal import reset_sync, sync
from models import ServiceProvider, ServiceProviderImage, User

from misc import MultiImageField, CustomImageField


class UserChangeForm(DefaultUserChangeForm):
    phone = forms.CharField(max_length=100, label=_('Phone Number'))
    premium = forms.BooleanField(label=_('Premium User'))
    coupons = forms.IntegerField(label=_('Coupons'))
    reservations = forms.IntegerField(label=_('Reservations'))


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label=_('First Name'))
    last_name = forms.CharField(max_length=30, label=_('Last Name'))
    phone = forms.CharField(max_length=100, label=_('Phone Number'))
    language = forms.ChoiceField(choices=settings.LANGUAGES, label=_('Language'))
    notification_type = forms.ChoiceField(choices=User.NOTIFICATION_TYPES_CHOICES)

    def save(self, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.language = self.cleaned_data['language']
        user.notification_type = self.cleaned_data['notification_type']
        user.save()

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('initial', {}).setdefault('language', 'en')
        super(SignupForm, self).__init__(*args, **kwargs)


class ServiceProviderForm(ModelForm):
    logo = forms.ImageField(widget=ClearableImageInput(), required=False)

    class Meta:
        model = ServiceProvider
        exclude = ('lat', 'lng', 'gcal_id', 'gcal_updated', 'logo_width', 'logo_height', 'subscription_end_date',
                   'subscription_mail_sent', 'subscription_end_date', 'display_generic_gallery', 'subscribers')

    def save(self, *args, **kwargs):
        if self.instance and self.instance.timezone != self.old_timezone:
            #print 'reset'
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
    image = CustomImageField(required=True, label=_('Upload images'))

    class Meta:
        model = ServiceProviderImage
        exclude = ('image_width', 'image_height', 'service_provider', 'delete_image')

    def __init__(self, *args, **kwargs):
        self.file_id = kwargs.pop('file_id', 0)
        super(ServiceProviderImageForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        if not super(ServiceProviderImageForm, self).is_valid():
            return False

        imageA = self.files.getlist('image') if not isinstance(self.files,dict) else self.files['image']

        if not imageA:
            self.error = _("No files")
            return False

        #imageA = images[0]
        if imageA.name == "logo.png":
            self.error = _("Artificial error")
            return False

        if imageA:
            if imageA._size > 15 * 1024 * 1024:
                self.error = _("Image bigger than 15MB!")
                return False

            return True
        else:
            self.error = _("Image is null!")
            return False


class ServiceProviderMultiImageHelperForm(Form):
    images = MultiImageField(required=True, label=_('Upload images'))

    def __init__(self, *args, **kwargs):
        super(ServiceProviderMultiImageHelperForm, self).__init__(*args, **kwargs)
        self.service_provider_forms = []
        self.error_list = []

        FIELDS = args[0] if args else None
        FILES = args[1] if args else None

        if FILES:
            if 'images' in FILES:
                for i, img in enumerate(FILES.getlist('images')):
                    self.service_provider_forms.append(ServiceProviderImageForm(FIELDS, {'image': [img]}, file_id=i))

ServiceProviderImageFormSet = formset_factory(ServiceProviderImageForm)
