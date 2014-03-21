import csv
import itertools
import os
import tempfile

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _

from enarocanje.accountext.decorators import for_service_providers
from enarocanje.service.models import Service
from forms import CouponForm, CsvForm
from models import Coupon

@for_service_providers
def mycoupons(request):
	coupons = request.user.service_provider.coupons.all()
	return render_to_response('coupon/mycoupons.html', locals(), context_instance=RequestContext(request))

@for_service_providers
def add(request):
	if request.method == 'POST':
		# if method was post (form submittion), fill form from post data
		form = CouponForm(request.POST, provider=request.user.service_provider)
		if form.is_valid():
			# if form is valid, save it and redirect back to myservices
			# commit=False tells form to not save the object to the database just yet and return it instead
			coupon = form.save(commit=False)
			# set service_provider to the current user before we save the object to the database
			coupon.service_provider = request.user.service_provider
			coupon.save()
			return HttpResponseRedirect(reverse(mycoupons))
	else:
		# on get request create empty form
		form = CouponForm(provider=request.user.service_provider)
		# render form - new (get request) or invalid with error messages (post request)
	return render_to_response('coupon/add.html', locals(), context_instance=RequestContext(request))

@for_service_providers
def edit(request, id):
	coupon = get_object_or_404(Coupon, service_provider=request.user.service_provider, id=id)
	if request.method == 'POST':
		form = CouponForm(request.POST, instance=coupon, provider=coupon.service_provider)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse(mycoupons))
	else:
		form = CouponForm(instance=coupon, provider=coupon.service_provider)
	return render_to_response('coupon/edit.html', locals(), context_instance=RequestContext(request))

@for_service_providers
def csv_upload(request):
	if request.method == 'POST':
		form = CsvForm(request.POST, request.FILES, provider=request.user.service_provider)
		if form.is_valid():
			# Parse the csv file
			try:
				csvf = csv.reader(request.FILES.get('file'))
				ok = 0
				fail = 0
				header = False
				coupons = []
				for i, row in enumerate(csvf):
					if not row:
						continue
					# Parse the row using form
					cf = CouponForm({
						'number': row[0],
						'valid': row[1],
						'service': form.cleaned_data['service'].id,
					}, provider=request.user.service_provider)
					# Check if it is valid
					if cf.is_valid():
						coupon = cf.save(commit=False)
						coupon.service_provider = request.user.service_provider
						coupons.append(coupon)
						ok += 1
					else:
						if i == 0:
							header = True
						else:
							fail += 1
			except:
				# Something went wrong (probably with parsing)
				messages.error(request, _('CSV parsing failed'))
				return HttpResponseRedirect(reverse(csv_upload))
			else:
				# Save created coupons
				for coupon in coupons:
					coupon.save()
				# Check ok and fail counters
				msg_end = u'.'
				if header:
					msg_end = u', ' + _('first row skipped') + u'.'
				if fail == 0:
					messages.success(request, _('%d coupons successfully parsed and created') % ok + msg_end)
				elif ok > 0:
					messages.warning(request, _('%d coupons successfully parsed and created, %d failed') % (ok, fail) + msg_end)
				else:
					messages.error(request, _('Coupon parsing failed. Check your format.'))
				return HttpResponseRedirect(reverse(mycoupons))
	else:
		form = CsvForm(provider=request.user.service_provider)
	return render_to_response('coupon/csvupload.html', locals(), context_instance=RequestContext(request))

@for_service_providers
def manage(request):
	if request.method == 'POST':
		coupon = get_object_or_404(Coupon, service_provider=request.user.service_provider, id=request.POST.get('coupon'))
		if request.POST.get('action') == 'delete':
			coupon.delete()
		if request.POST.get('action') == 'deleteAll':
			coupons = request.user.service_provider.coupons.all()
			coupons.delete()
			return HttpResponseRedirect(reverse(mycoupons))
	return HttpResponseRedirect(reverse(mycoupons))

def manageall(request):
	if request.method == 'POST':
		if request.POST.get('action') == 'deleteAll':
			coupons = request.user.service_provider.coupons.all()
			coupons.delete()
	return HttpResponseRedirect(reverse(mycoupons))
