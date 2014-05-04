import sys
from django.shortcuts import render
from django.core.mail import send_mail
from enarocanje.accountext.models import ServiceProvider

def newsletter(request):
    return render(request, 'newsletter/mynewsletter.html')

def send(request):
    if request.method == "POST":
        subject = request.POST['subject']
        message = request.POST['newsletter']
        provider = ServiceProvider.objects.get(name=request.user.service_provider.name)
        subscribers = provider.subscribers.all()
        emails = [user.email for user in subscribers]
        send_mail(subject, message, request.user.email, 
                  emails, fail_silently=False)
        return render(request, 'newsletter/sent.html')
    else:
        return render(request, 'newsletter/post.html')