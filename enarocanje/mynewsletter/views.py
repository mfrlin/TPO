from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from enarocanje.accountext.models import ServiceProvider
from django.utils.translation import ugettext_lazy as _


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
        return render(request, 'newsletter/mynewsletter.html',
                      {'message': _('Your message has been send to all of your subscribers.')})
    else:
        return render(request, 'newsletter/post.html',
                      {'message': _('You should use the form at \'Send a newsletter\' to send newsletters.')})