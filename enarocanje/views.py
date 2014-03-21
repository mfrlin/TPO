from django.shortcuts import render_to_response
from django.template import RequestContext

from service.models import Service, Category

def home(request):
	return render_to_response('main.html', locals(), context_instance=RequestContext(request))
