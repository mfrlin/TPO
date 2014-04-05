import datetime
import json
import urllib
import re
import base64

from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.images import ImageFile
from django.core.files.base import ContentFile

from cStringIO import StringIO

from enarocanje.accountext.decorators import for_service_providers
from enarocanje.accountext.forms import ServiceProviderImageForm,ServiceProviderMultiImageHelperForm
from enarocanje.accountext.models import ServiceProvider, ServiceProviderImage, Category as SPCategory
from enarocanje.service.models import Category as ServiceCategory, Service
from enarocanje.reservations.models import Reservation
from forms import ServiceForm, FilterForm, DiscountFormSet, CommentForm
from models import Service, Category, Discount, Comment

import enarocanje.common.config as config
# List of services for editing


def view_gallery(request, id):
    GENERIC_GALLERY_URL = config.GENERIC_GALLERY_URL
    
    service_provider = ServiceProvider.objects.get(id=id)
    service_provider_category = service_provider.category
    
    generic_gallery = None
    generic_gallery_id_name = None
    if(service_provider_category):
        generic_gallery_id_name = service_provider_category.generic_gallery
        if(generic_gallery_id_name):
            generic_gallery = config.GENERIC_GALLERY_IMAGES[generic_gallery_id_name] \
                if generic_gallery_id_name in config.GENERIC_GALLERY_IMAGES \
                else {'title':service_provider_category.name, 'values':[]}
 
    service_categories = ServiceCategory.objects.filter(show_in_gallery=True)
    cheapest_service = None
    best_service = None
    for service_category in service_categories:
        services = Service.objects.filter(category=service_category)
        for service in services:            
            if cheapest_service:
                if cheapest_service.discounted_price() > service.discounted_price():
                    cheapest_service = service
            
            if best_service:
                if best_service.discounted_price() < service.discounted_price():
                    best_service = service
                    
            if cheapest_service is None:
                cheapest_service = service

            if best_service is None:
                best_service = service
 
    foto_services = filter(lambda x: x is not None,[best_service, cheapest_service])
 
    gallery = ServiceProviderImage.objects.filter(service_provider_id=id)
    # ServiceProviderImage.objects.all().delete()
    edit_gallery = False
    # print "id, provID", id, request.user.service_provider_id
    if hasattr(request.user, 'service_provider_id'):
        if str(id) == str(request.user.service_provider_id):
            edit_gallery = True

    if request.method == 'POST':
        if request.POST.get('action') == 'delete':
            form = ServiceProviderMultiImageHelperForm()
            if request.POST.getlist('img_id'):
                for img_id in request.POST.getlist('img_id'):
                    print "iiid", img_id
                    img = ServiceProviderImage.objects.get(id=int(img_id))
                    img.delete()

        if request.POST.get('action') == 'enable_generic_gallery':
            form = ServiceProviderMultiImageHelperForm()
            service_provider.display_generic_gallery = True
            service_provider.save()
            
        if request.POST.get('action') == 'disable_generic_gallery':
            form = ServiceProviderMultiImageHelperForm()
            service_provider.display_generic_gallery = False
            service_provider.save()

        if request.POST.get('action') == 'upload_photo':
            form = ServiceProviderMultiImageHelperForm()

            error_msg = None

            dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
            ImageData = request.POST.get('captured_photo')
            if ImageData:
                ImageData = dataUrlPattern.match(ImageData).group(2)

                if not (ImageData == None or len(ImageData) == 0):
                    ImageData = base64.b64decode(ImageData)
                    
                    buf = StringIO(ImageData)
                    buf.seek(0, 2)
                    
                    from time import time
                    
                    file = InMemoryUploadedFile(buf, None, 'captured_image_'+str(time())+'.jpg', 'image/jpeg', buf.tell(), None)
                    buf.seek(0)

                    file.seek(0)
                    helper_form = ServiceProviderImageForm(request.POST, {'image':[file]})
                    if helper_form.is_valid():
                        image = helper_form.save(commit=False)
                        image.service_provider_id = request.user.service_provider_id
                        image.save()
                    else:
                        form.error_list.append(helper_form.errors)

                else:
                    error_msg = _("Error during decoding")
            else:
                error_msg = _("No image was submited")
                

        if request.POST.get('action') == 'update':
            form = ServiceProviderMultiImageHelperForm(request.POST, request.FILES)
            
            print form.service_provider_forms
            for uploaded_file_form in form.service_provider_forms:
                if uploaded_file_form.is_valid():
                    image = uploaded_file_form.save(commit=False)
                    image.service_provider_id = request.user.service_provider_id
                    image.save()
                else:
                    form.error_list.append(uploaded_file_form.errors)


    else:
        form = ServiceProviderMultiImageHelperForm()

    return render_to_response('browse/gallery.html', locals(), context_instance=RequestContext(request))


@for_service_providers
def myservices(request):
    services = request.user.service_provider.services.all()
    durations = set(service.duration for service in services)
    # discounts = set(service.get_discount().discount for service in services if service.get_discount())
    discounts = set(discount.discount for discount in Discount.objects.filter(service__in=services))
    filter_form = FilterForm(request.GET, durations=sorted(list(durations)), discounts=discounts)
    if filter_form.is_valid():
        if filter_form.cleaned_data['duration'] != 'all':
            services = services.filter(duration=filter_form.cleaned_data['duration'])
        if filter_form.cleaned_data['discount'] != 'all':
            services = services.filter(discounts__discount=filter_form.cleaned_data['discount']).distinct()
        if filter_form.cleaned_data['active'] == 'active':
            services = [service for service in services if service.is_active()]
        elif filter_form.cleaned_data['active'] == 'inactive':
            services = [service for service in services if not service.is_active()]
    # locals() returns a dictionary of variables in the local scope (request and services in this case)
    return render_to_response('service/myservices.html', locals(), context_instance=RequestContext(request))

# Add a new service


@for_service_providers
def add(request):
    if request.method == 'POST':
        # if method was post (form submittion), fill form from post data
        form = ServiceForm(request.POST)
        form_valid = form.is_valid()
        formset = DiscountFormSet(request.POST)
        formset_valid = formset.is_valid()
        if form_valid and formset_valid:
            # if form is valid, save it and redirect back to myservices
            # commit=False tells form to not save the object to the database just yet and return it instead
            service = form.save(commit=False)
            # set service_provider to the current user before we save the object to the database
            service.service_provider = request.user.service_provider
            service.save()
            formset.instance = service
            formset.save()
            return HttpResponseRedirect(reverse(myservices))
    else:
        # on get request create empty form
        form = ServiceForm()
        formset = DiscountFormSet()
    # render form - new (get request) or invalid with error messages (post request)
    return render_to_response('service/add.html', locals(), context_instance=RequestContext(request))

# Edit existing service


@for_service_providers
def edit(request, id):
    service = get_object_or_404(Service, service_provider=request.user.service_provider, id=id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        form_valid = form.is_valid()
        formset = DiscountFormSet(request.POST, instance=service)
        formset_valid = formset.is_valid()
        if form_valid and formset_valid:
            form.save()
            formset.save()
            return HttpResponseRedirect(reverse(myservices))

    else:
        form = ServiceForm(instance=service)
        formset = DiscountFormSet(instance=service)
    return render_to_response('service/edit.html', locals(), context_instance=RequestContext(request))

# Activate/deactivate service


@for_service_providers
def manage(request):
    if request.method == 'POST':
        service = get_object_or_404(Service, service_provider=request.user.service_provider,
                                    id=request.POST.get('service'))
        if request.POST.get('action') == 'activate':
            service.active_until = None
            service.save()
        if request.POST.get('action') == 'deactivate':
            service.active_until = datetime.date.today() - datetime.timedelta(1)
            service.save()
        if request.POST.get('action') == 'delete':
            service.delete()
    return HttpResponseRedirect(reverse(myservices))

# Individual service


def service_comments(request, id):
    service = get_object_or_404(Service, id=id)
    if not service.is_active():
        raise Http404

    # check if user is allowed to comment
    if request.user.is_authenticated():
        now = datetime.datetime.now()
        reservations = Reservation.objects.filter(Q(user=request.user, service=service) & (
        Q(date__lt=now.date()) | Q(date=now.date(), time__lt=now.time()))).order_by('-date', '-time')
        if len(reservations) and not Comment.objects.filter(author=request.user, service=service,
                                                            created__gt=datetime.datetime.combine(reservations[0].date,
                                                                                                  reservations[
                                                                                                      0].time)).exists():
            # handle form
            if request.method == 'POST':
                form = CommentForm(request.POST)
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.service = service
                    comment.author = request.user
                    comment.save()
                    return HttpResponseRedirect(reverse(service_comments, args=(id,)))
            else:
                form = CommentForm()

    # get all comments
    comments = service.comments.order_by('-created').all()

    return render_to_response('service/comments.html', locals(), context_instance=RequestContext(request))

# Browse


def int_get(d, k):
    try:
        return int(d[k])
    except:
        return None


def get_location(request):
    try:
        location = request.COOKIES.get('location')
        location = urllib.unquote(location)
        location = json.loads(location)
        location['lat'] = float(location['lat'])
        location['lng'] = float(location['lng'])
        location['accuracy'] = float(location['accuracy'])
    except:
        location = None
    return location


ORDER_CHOICES_PROVIDER = (
(_('Order by distance'), 'dist'),
(_('Order lexicographically'), 'lexi'),
)


def construct_url_providers(cat, q, sor, page):
    parts = []
    if cat:
        parts.append('category=%d' % cat)
    if q:
        parts.append('q=%s' % q)
    if sor != 'dist':
        parts.append('sort=%s' % sor)
    if page:
        parts.append('page=%s' % page)
    if parts:
        return '?' + '&'.join(parts)
    return reverse(browse_providers)


def browse_providers(request):
    location = get_location(request)
    providers = ServiceProvider.objects.all()

    if hasattr(request.user, 'has_service_provider'):
        if request.user.has_service_provider():
            provider = ServiceProvider.objects.get(id=request.user.service_provider_id)
            if provider.subscription_end_date < timezone.now():
                if not provider.subscription_mail_sent:
                    send_mail('Subscription expirations', 'Sorry to inform you but your subscription has expired.',
                              'from@example.com',
                              [request.user.email], fail_silently=False)
                provider.subscription_mail_sent = 1
                provider.save()

    cat = int_get(request.GET, 'category')
    q = request.GET.get('q', '')
    sor = request.GET.get('sort', 'dist')
    page = request.GET.get('page')

    categories = [(_('All'), construct_url_providers(None, q, sor, page), not cat)] + [
        (category.name, construct_url_providers(category.id, q, sor, page), category.id == cat)
        for category in SPCategory.objects.all()
    ]
    sort_choices = [
        (sort[0], construct_url_providers(cat, q, sort[1], page), sort[1] == sor)
        for sort in ORDER_CHOICES_PROVIDER
    ]

    if cat:
        providers = providers.filter(category_id=cat)
    if q:
        providers = providers.filter(name__search=q)

    # Order by
    if sor == 'dist':
        if location and settings.DATABASE_SUPPORTS_TRIGONOMETRIC_FUNCTIONS:
            providers = providers.extra(select={'dist': ServiceProvider.DISTANCE_FORMULA % location}).order_by('dist')
    elif sor == 'lexi':
        providers = providers.order_by('name')

    paginator = Paginator(providers, 12)
    try:
        providers = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        providers = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        providers = paginator.page(paginator.num_pages)

    if providers.has_previous():
        prev_page = construct_url_providers(cat, q, sor, providers.previous_page_number())
    if providers.has_next():
        next_page = construct_url_providers(cat, q, sor, providers.next_page_number())

    return render_to_response('browse/providers.html', locals(), context_instance=RequestContext(request))


SORT_CHOICES_SERVICE = (
(_('Order by distance'), 'dist'),
(_('Order by price'), 'price'),
(_('Order by discount level'), 'disc'),
(_('Order lexicographically'), 'lexi'),
(_('Last ordered'), 'reserv'),
(_('My last ordered'), 'myres'),
)


def construct_url_services(prov, cat, disc, q, sor, page):
    parts = []
    if prov:
        parts.append('provider=%d' % prov)
    if cat:
        parts.append('category=%d' % cat)
    if disc:
        parts.append('discount=%d' % disc)
    if q:
        parts.append('q=%s' % q)
    if sor != 'dist':
        parts.append('sort=%s' % sor)
    if page:
        parts.append('page=%s' % page)
    if parts:
        return '?' + '&'.join(parts)
    return reverse(browse_services)

def browse_services(request):
    location = get_location(request)
    services = Service.objects.filter(Q(active_until__gte=datetime.date.today()) | Q(active_until__isnull=True))

    prov = int_get(request.GET, 'provider')
    cat = int_get(request.GET, 'category')
    disc = int_get(request.GET, 'discount')
    q = request.GET.get('q', '')
    sor = request.GET.get('sort', 'dist')
    page = request.GET.get('page')

    categories = [(_('All'), construct_url_services(prov, None, disc, q, sor, page), not cat)] + [
        (category.name, construct_url_services(prov, category.id, disc, q, sor, page), category.id == cat)
        for category in Category.objects.all()
    ]
    discounts = [(_('All'), construct_url_services(prov, cat, None, q, sor, page), not disc)] + [
        ('%s%%' % discount, construct_url_services(prov, cat, discount, q, sor, page), discount == disc)
        for discount in set(
            service.get_discount().discount
            for service in services if service.get_discount()
        )
    ]
    sort_choices = [
        (sort[0], construct_url_services(prov, cat, disc, q, sort[1], page), sort[1] == sor)
        for sort in SORT_CHOICES_SERVICE
    ]

    if cat:
        services = services.filter(category_id=cat)
    selected_provider = None
    if prov:
        selected_provider = get_object_or_404(ServiceProvider, id=prov)
        services = services.filter(service_provider_id=prov)
    if q:
        services = services.filter(Q(name__search=q) | Q(description__search=q))

    # Order by
    if sor == 'dist':
        if location and settings.DATABASE_SUPPORTS_TRIGONOMETRIC_FUNCTIONS:
            services = services.select_related('service_provider').extra(
                select={'dist': ServiceProvider.DISTANCE_FORMULA % location}).order_by('dist')
    elif sor == 'price':
        # TODO: sort in database
        services = sorted(services,
                          lambda a, b: cmp(a.discounted_price() or float('inf'), b.discounted_price() or float('inf')))
    elif sor == 'disc':
        # TODO: sort in database
        services = sorted(services, lambda a, b: cmp(a.get_discount().discount if a.get_discount() else 0,
                                                     b.get_discount().discount if b.get_discount() else 0),
                          reverse=True)
    elif sor == 'lexi':
        services = services.order_by('name')
        
    elif sor == 'reserv':
        services = []
        if cat:
            for x in Category.objects.filter(id=cat): # iz vsake kategorije
                [services.append(y.service)
                    for y in Reservation.objects.filter(service__category=x)
                    .order_by('-date', '-time')
                ] # 3 nazadnje rezerviranih storitev
        else:
            for x in Category.objects.all(): # iz vsake kategorije
                [services.append(y.service)
                    for y in Reservation.objects.filter(service__category=x)
                    .order_by('-date', '-time')
                ] # 3 nazadnje rezerviranih storitev
        services = services[:3]

    elif sor == 'myres':
        services = []
        if cat and request.user.is_authenticated():
            for x in Category.objects.filter(id=cat): # iz vsake kategorije
                [services.append(y.service)
                    for y in Reservation.objects.filter(service__category=x, user=request.user)
                    .order_by('-date', '-time')
                ] # 3 nazadnje rezerviranih storitev
        elif request.user.is_authenticated():
            for x in Category.objects.all(): # iz vsake kategorije
                [services.append(y.service)
                    for y in Reservation.objects.filter(service__category=x, user=request.user)
                    .order_by('-date', '-time')
                ] # 3 nazadnje rezerviranih storitev
        services = services[:3]

    if disc:
        services = [service for service in services if
                    service.get_discount() and service.get_discount().discount == disc]

    paginator = Paginator(services, 12)
    try:
        services = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        services = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        services = paginator.page(paginator.num_pages)

    if services.has_previous():
        prev_page = construct_url_services(prov, cat, disc, q, sor, services.previous_page_number())
    if services.has_next():
        next_page = construct_url_services(prov, cat, disc, q, sor, services.next_page_number())

    return render_to_response('browse/services.html', locals(), context_instance=RequestContext(request))


@for_service_providers
def managereservation(request):
    if request.method == 'POST':
        reservation = get_object_or_404(Reservation, service_provider=request.user.service_provider,
                                        id=request.POST.get('reservation'))
        if request.POST.get('action') == 'confirm':
            reservation.is_confirmed = True
            reservation.save()
            if not reservation.user:
                email_to1 = reservation.user_email
            else:
                email_to1 = reservation.user.email
            subject = _('Confirmation of service reservation')
            renderedToCustomer = render_to_string('emails/reservation_customer.html', {'reservation': reservation})
            send_mail(subject, renderedToCustomer, 'none', [email_to1], fail_silently=False)
        if request.POST.get('action') == 'deny':
            reservation.is_deny = True
            reservation.save()
            if not reservation.user:
                email_to1 = reservation.user_email
            else:
                email_to1 = reservation.user.email
            subject = _('Your reservation was not confirmed')
            renderedToCustomer = render_to_string('emails/reservation_customer.html', {'reservation': reservation})
            send_mail(subject, renderedToCustomer, 'none', [email_to1], fail_silently=False)
            reservation.delete()
    return HttpResponseRedirect(reverse(myunconfirmedreservations))


def managereservationall(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'confirmall':
            reservations = request.user.service_provider.reservations.filter(
                service_provider_id=request.user.service_provider_id, is_confirmed=False, is_deny=False,
                isfromgcal=False, date__gte=datetime.date.today())
            for res in reservations:
                res.is_confirmed = True
                res.save()
                if not res.user:
                    email_to1 = res.user_email
                else:
                    email_to1 = res.user.email
                subject = _('Confirmation of service reservation')
                renderedToCustomer = render_to_string('emails/reservation_customer.html', {'reservation': res})
                send_mail(subject, renderedToCustomer, None, [email_to1], fail_silently=False)
        if request.POST.get('action') == 'denyall':
            reservations = request.user.service_provider.reservations.filter(
                service_provider_id=request.user.service_provider_id, is_confirmed=False, is_deny=False,
                isfromgcal=False, date__gte=datetime.date.today())
            for res in reservations:
                res.is_deny = True
                res.save()
                if not res.user:
                    email_to1 = res.user_email
                else:
                    email_to1 = res.user.email
                subject = _('Your reservation was not confirmed')
                renderedToCustomer = render_to_string('emails/reservation_customer.html', {'reservation': res})
                send_mail(subject, renderedToCustomer, None, [email_to1], fail_silently=False)
                res.delete()
    return HttpResponseRedirect(reverse(myunconfirmedreservations))


@for_service_providers
def myunconfirmedreservations(request):
    res_confirm = request.user.service_provider.reservation_confirmation_needed
    unconfirmed = Reservation.objects.filter(service_provider_id=request.user.service_provider_id, is_confirmed=False,
                                             is_deny=False, date__gte=datetime.date.today(), isfromgcal=False)
    return render_to_response('service/myunconfirmedreservation.html', locals(),
                              context_instance=RequestContext(request))
