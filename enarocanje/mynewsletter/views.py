from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from enarocanje.accountext.models import ServiceProvider
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from models import Newsletter
from django.views.generic import ListView
import sys

class ListNewsletterView(ListView):
    model = Newsletter
    template_name = 'newsletter/newsletterlist.html'
    
    def get_queryset(self):
        return Newsletter.objects.order_by('-date_sent')
    
    """def get_context_data(self, **kwargs):
        context = super(ListNewsletterView, self).get_context_data(**kwargs)
        return context"""

def newsletter(request):
    return render(request, 'newsletter/mynewsletter.html')


def send(request):
    if request.method == "POST":
        subject = request.POST['subject']
        message = request.POST['newsletter']
        provider = ServiceProvider.objects.get(name=request.user.service_provider.name)
        
        # inform the subscribers, according to some criteria
        number_of_coupons = request.POST['coupons']
        number_of_reservations = request.POST['reservations']
        
        if number_of_coupons == "low":
            low_coupons = 0
            high_coupons = 20
        elif number_of_coupons == "medium":
            low_coupons = 21
            high_coupons = 40
        elif number_of_coupons == "high":
            low_coupons = 41
            high_coupons = sys.maxint
        
        if number_of_reservations == "low":
            low_reservations = 0
            high_reservations = 20
        elif number_of_reservations == "medium":
            low_reservations = 21
            high_reservations = 40
        elif number_of_reservations == "high":
            low_reservations = 41
            high_reservations = sys.maxint
        
        if number_of_coupons == "any" and number_of_reservations == "any":
            subscribers = provider.subscribers.all()
        elif number_of_coupons == "any":
            subscribers = provider.subscribers.filter(
                reservations__range=(low_reservations, high_reservations))
        elif number_of_reservations == "any":
            subscribers = provider.subscribers.filter(
                coupons__range=(low_coupons, high_coupons))
        else:
            subscribers = provider.subscribers.filter(
                reservations__range=(low_reservations, high_reservations),
                coupons__range=(low_coupons, high_coupons))
        
        emails = [user.email for user in subscribers]
        try:
            send_mail(subject, message, request.user.email,
                      emails, fail_silently=False)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        
        # save the message in the db
        # subject, message, provider, number_of_subscribers
        newsletter = Newsletter(
                                provider=request.user.service_provider,
                                date_sent=timezone.now(),
                                subject=subject,
                                message=message,
                                number_of_subscribers=len(subscribers)
                                )
        newsletter.save()
        return render(request, 'newsletter/mynewsletter.html',
                      {'message': _('Your message has been sent to all of your subscribers.')})
    else:
        return render(request, 'newsletter/post.html',
                      {'message': _('You should use the form at \'Send a newsletter\' to send newsletters.')})