from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from enarocanje.accountext.models import ServiceProvider
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from models import Newsletter
from django.views.generic import ListView

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
        subscribers = provider.subscribers.all()
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