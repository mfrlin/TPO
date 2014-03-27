from django.shortcuts import render_to_response
from django.template import RequestContext


def home(request):
    return render_to_response('main.html', locals(), context_instance=RequestContext(request))


def cookies(request):
    return render_to_response('browse/cookies.html', locals(), context_instance=RequestContext(request))