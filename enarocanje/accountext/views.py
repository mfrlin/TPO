from allauth.account.utils import complete_signup
from allauth.account.views import SignupView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from forms import SignupForm, ServiceProviderForm
from models import User, ServiceProvider


@login_required
def account_profile(request):
    if request.POST.get('action') == 'makeprovider' and not request.user.has_service_provider():
        request.user.service_provider = ServiceProvider.objects.create(name='Unnamed Service Provider')
        request.user.service_provider.save()
        request.user.save()
        return HttpResponseRedirect('')
    if request.POST.get('action') == 'removeprovider' and request.user.has_service_provider():
        service_provider = request.user.service_provider
        request.user.service_provider = None
        request.user.save()
        service_provider.delete()
        return HttpResponseRedirect('')

    initial = {
    'first_name': request.user.first_name,
    'last_name': request.user.last_name,
    'phone': request.user.phone,
    'language': request.user.language,

    }

    if request.user.service_provider:
        lat = request.user.service_provider.lat
        lng = request.user.service_provider.lng

    if request.method == "POST":
        form = SignupForm(request.POST, initial=initial)
        service_provider_form = ServiceProviderForm(request.POST, request.FILES, instance=request.user.service_provider)
        if form.is_valid() and service_provider_form.is_valid():
            form.save(request.user)
            service_provider_form.save()
            request.session['django_language'] = request.user.language
            return HttpResponseRedirect('')
    else:
        form = SignupForm(initial=initial)
        service_provider_form = ServiceProviderForm(instance=request.user.service_provider)

    return render_to_response('account/profile.html', locals(), context_instance=RequestContext(request))


@receiver(user_logged_in)
def lang(sender, request, user, **kwargs):
    request.session['django_language'] = user.language


class SignupView2(SignupView):
    def dispatch(self, request, *args, **kwargs):
        if 'referral' in request.GET:
            request.session['referral'] = request.GET['referral']
        return super(SignupView2, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(self.request)
        try:
            user.referral = User.objects.get(id=self.request.session['referral'])
        except KeyError:
            pass
        except ValueError:
            pass
        except ObjectDoesNotExist:
            pass
        user.save()
        return complete_signup(self.request, user, self.get_success_url())


signup = SignupView2.as_view()
