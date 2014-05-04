from django.shortcuts import render
from django.core.mail import send_mail
from enarocanje.celery import app
from enarocanje.accountext.models import ServiceProvider

def newsletter(request):
    return render(request, 'newsletter/mynewsletter.html')

def send(request):
    if request.method == "POST":
        subject = request.POST['subject']
        message = request.POST['newsletter']
        subscribers = ServiceProvider.objects.filter(subscribers__subscribed=True)
        emails = [email for email in subscribers.user.email]
        results = send_it.delay(subject, message, request.user.email, emails)
        if results.ready():
            return render(request, 'newsletter/sent.html')
        else:
            results.get(timeout=30)
            return render(request, 'newsletter/sent.html') 

@app.task
def send_it(subject, message, sender, receivers):
    send_mail(subject, message, 'simon.stoiljkovikj@gmail.com', 
                  ['ss2460@student.uni-lj.si'], fail_silently=False)