import datetime
import json
import urllib
import re
import base64

import operator

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

from enarocanje.accountext.decorators import for_service_providers
from enarocanje.accountext.forms import ServiceProviderImageForm, ServiceProviderMultiImageHelperForm
from enarocanje.accountext.models import ServiceProvider, ServiceProviderImage, Category as SPCategory, User
from enarocanje.service.models import Service, Category, Discount, Comment
from enarocanje.reservations.models import Reservation

from enarocanje.workinghours.models import WorkingHours, WorkingHoursBreak, Absence, DAYS_OF_WEEK_DICT

import enarocanje.common.config as config
# List of services for editing


def userpage_main(request, user_link):
    GENERIC_GALLERY_URL = config.GENERIC_GALLERY_URL

    selected_provider = get_object_or_404(ServiceProvider, userpage_link=user_link)

    provider_user = User.objects.get(service_provider=selected_provider)

    #location = get_location(request)
    services = Service.objects.filter(Q(active_until__gte=datetime.date.today()) | Q(active_until__isnull=True))
    services = services.filter(service_provider_id=selected_provider.id)

    gallery = ServiceProviderImage.objects.filter(service_provider_id=selected_provider.id)

    categories = Category.objects.all()

    #    categorized_services = {}

    cats = dict(map(lambda x: (x.id, x.name), categories))

    #    for service in services:
    #        if service.category_id in categorized_services:
    #            categorized_services[service.category_id][1].append(service)
    #        else:
    #            categorized_services[service.category_id] \
    #                = (cats[service.category_id] if service.category_id in cats else None, [service])

    page_size = 10

    prev_cat_id = -1
    cc = 0

    services_list_sorted_by_cat = sorted(list(services), key=operator.attrgetter('category_id'))

    services_pages = []
    for i, service in enumerate(services_list_sorted_by_cat):

        if i % page_size == 0:
            prev_cat_id = -1
            services_pages.append([])
        page = services_pages[-1]

        paged_category = None
        if service.category_id != prev_cat_id:
            prev_cat_id = service.category_id

            paged_category = {'category_id': service.category_id,
                              'category_name': cats[service.category_id] if service.category_id in cats else  None,
                              'services': []}
            page.append(paged_category)

        paged_category = page[-1]

        paged_category['services'].append(service)

    #dxx = json.dumps(services_pages, sort_keys=True, indent=4, separators=(',', ': '))

    service_provider_category = selected_provider.category

    generic_gallery = None
    generic_gallery_id_name = None

    if selected_provider.display_generic_gallery:
        if service_provider_category:
            generic_gallery_id_name = service_provider_category.generic_gallery
            if generic_gallery_id_name:
                if generic_gallery_id_name in config.GENERIC_GALLERY_IMAGES:
                    generic_gallery = config.GENERIC_GALLERY_IMAGES[generic_gallery_id_name]
                    generic_gallery = generic_gallery['values']
                else:
                    generic_gallery = {'title': service_provider_category.name, 'values': []}

    working_hours = WorkingHours.objects.filter(service_provider=selected_provider)

    wkdys = dict()
    wkdys[1] = set([])
    wkdys[2] = set([])
    wkdys[3] = set([])
    wkdys[4] = set([])
    wkdys[5] = set([])
    wkdys[6] = set([])
    wkdys[7] = set([])

    for wh in working_hours:
        wh_breaks = WorkingHoursBreak.objects.filter(working_hours=wh)

        for week_day in map(int, wh.week_days_list()):
            wkdys[week_day].add(wh.time_from)
            wkdys[week_day].add(wh.time_to)

            for wh_b in wh_breaks:
                wkdys[week_day].add(wh_b.time_from)
                wkdys[week_day].add(wh_b.time_to)

    working_hours_blocks = []
    for k, v in wkdys.iteritems():
        tuples = []
        v = sorted(list(v))
        for i in range(0, len(v), 2):
            tuples.append((v[i], v[i + 1]))

        working_hours_blocks.append((k, DAYS_OF_WEEK_DICT[str(k)], tuples))


    lat = selected_provider.lat
    lng = selected_provider.lng

    return render_to_response('userpages/provider_page.html', locals(), context_instance=RequestContext(request))



