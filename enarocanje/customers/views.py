from django.core.urlresolvers import reverse
from django.views.generic import UpdateView, CreateView, ListView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponse

from .models import Customer
from .forms import CustomerForm, ExportListForm, UploadFileForm, ChoiceRowForm
from enarocanje.accountext.decorators import for_service_providers
from enarocanje.reservations.models import Reservation

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from banana_py import Bananas_OAuth


import csv
import xlrd

import re
import os

import mailchimp



@for_service_providers
def import_customers(request):
    row_choice = ChoiceRowForm();

    if request.POST.get('action') == 'upload':


        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            
            fileName, fileExtension = os.path.splitext(request.FILES.get('file').name)
            
            if fileExtension.lower() == '.csv':
                usrs2 = list(csv.reader(request.FILES.get('file'), delimiter=str(form.cleaned_data['delimiter'])[0],
                                    quotechar=str(form.cleaned_data['quote'])[0]))
                                    
                max_col_count = max(map(len, usrs2))
                
            elif fileExtension.lower() == '.xls':
                
                book = xlrd.open_workbook(file_contents=request.FILES.get('file').read())
                
                sheet = book.sheet_by_index(0)

                usrs2 = [[sheet.cell_value(row, col) for col in range(sheet.ncols)] for row in range(sheet.nrows) ]
                
                max_col_count = sheet.ncols

            usrs = []
            for v in usrs2:
                dt = max_col_count - len(v)
                if dt > 0:
                    v = v + [''] * dt

                usrs.append(v)

            row_count = len(usrs)

    elif request.POST.get('action') == 'import':
        form = UploadFileForm()

        data_num = request.POST.get('data_num')

        col_num = int(request.POST.get('max_col_count'))

        mapping = {}
        for j in range(col_num):
            mapping[j] = request.POST.get('id_selected_mapping_' + str(j))

        inv_mapping = dict(map(lambda x: (x[1], x[0],), mapping.items()))

        cc_updated = 0
        cc_created = 0
        cc_failed = 0
        for i in range(int(data_num)):
            if not request.POST.get('use_' + str(i + 1)):
                continue

            dasta = {'name': None, 'email': None, 'phone': None}

            for j in range(col_num):
                val = request.POST.get('row_' + str(i + 1) + '_col_' + str(j + 1))

                if mapping[j] == '0':
                    dasta['name'] = val
                elif mapping[j] == '1':
                    dasta['email'] = val
                elif mapping[j] == '2':
                    dasta['phone'] = val

                    #print mapping[j],j,val

            if dasta['email'] is None or (
                        dasta['email'] is not None and not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
                                                                    dasta['email'])):
                msg = _("Invalid emails")
                cc_failed += 1
                continue

            try:
                customer = Customer.objects.get(service=request.user.service_provider, email=dasta['email'])
            except:
                customer = None

            if not customer:
                customer = Customer()
                customer.service = request.user.service_provider
                customer.name = dasta['name']
                customer.phone = dasta['phone']
                customer.email = dasta['email']

                customer.save()

                cc_created += 1
            else:
                customer.name = dasta['name']
                customer.phone = dasta['phone']

                customer.save()

                cc_updated += 1
        status = True
    else:
        form = UploadFileForm()

    return render_to_response('customers/customer_list_import.html', locals(), context_instance=RequestContext(request))


@for_service_providers
def export_customers(request):
    if not 'mailchimp_details' in request.session:
        return HttpResponseRedirect(Bananas_OAuth().authorize_url())

    mc_stuff = request.session['mailchimp_details']

    api_key = mc_stuff['access_token']
    dc = mc_stuff['dc']

    mc_ = mailchimp.Mailchimp(apikey=api_key + '-' + dc)

    try:
        mc_.helper.ping()
    except mailchimp.Error:
        print "Invalid API key"

        return HttpResponseRedirect(reverse('mycustomers'))

    lists = mc_.lists.list()

    ll = (map(lambda x: (x['id'], x['name']), lists[u'data']))

    if request.POST.get('action') == 'export':
        export_list = ExportListForm(request.POST)
        export_list.fields['selected_list_id'].choices = ll
        if export_list.is_valid():
            provider = request.user.service_provider

            query = Customer.objects.filter(service=provider)

            batch = []

            for c in query:
                batch.append({'email': {'email': c.email}, 'email_type': 'html', 'merge_vars': {}})

            #batch_subscribe(export_list.selected_list_id)
            list_id = (export_list.cleaned_data['selected_list_id'])

            status = mc_.lists.batch_subscribe(list_id, batch)

    else:
        export_list = ExportListForm()
        export_list.fields['selected_list_id'].choices = ll

    return render_to_response('customers/customer_list_export.html', locals(), context_instance=RequestContext(request))


class ListCustomerView(ListView):
    model = Customer
    template_name = 'customer_list.html'

    def get_queryset(self):
        provider = self.request.user.service_provider
        sort_by = self.request.GET.get('sort_by', 'name')
        search_by = self.request.GET.get('search_by', '')
        name = Q(name__iregex=search_by)
        email = Q(email__iregex=search_by)
        phone = Q(phone__regex=search_by)
        if search_by:
            query = Customer.objects.filter(name | email | phone, service=provider)
        else:
            query = Customer.objects.filter(service=provider)
        if sort_by == 'name':
            return query.extra(
                select={'lower_name': 'lower(name)'}).order_by('lower_name')
        else:
            return query.order_by('-last_reservation')

    def get_context_data(self, **kwargs):
        context = super(ListCustomerView, self).get_context_data(**kwargs)
        if self.request.GET.get('search_by'):
            context['search_by'] = self.request.GET.get('search_by')
        return context


class ListCustomerReservations(ListView):
    model = Reservation
    template_name = 'customers/reservations_list.html'

    def get_queryset(self):
        try:
            user = Customer.objects.get(pk=self.kwargs.get('pk', -1)).user
        except:
            user = -1
        return Reservation.objects.filter(user=user, service_provider=self.request.user.service_provider)

    def get_context_data(self, **kwargs):
        context = super(ListCustomerReservations, self).get_context_data(**kwargs)
        customer = Customer.objects.get(id=self.kwargs.pop('pk')).__unicode__()
        context['customer'] = customer
        return context


class EditCustomerView(UpdateView):
    model = Customer
    template_name = 'customers/edit_customer.html'
    form_class = CustomerForm

    def get_success_url(self):
        return reverse('mycustomers')


class CreateCustomerView(CreateView):
    model = Customer
    template_name = 'customers/edit_customer.html'
    form_class = CustomerForm

    def get_success_url(self):
        return reverse('mycustomers')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.service = self.request.user.service_provider
        obj.save()
        return super(CreateCustomerView, self).form_valid(form)


@for_service_providers
def managecustomer(request):
    if request.method == 'POST':
        customer = get_object_or_404(Customer, service=request.user.service_provider,
                                     id=request.POST.get('service'))
        if request.POST.get('action') == 'delete':
            customer.delete()
    return HttpResponseRedirect(reverse('mycustomers'))


def showup(request):
    res = Reservation.objects.get(id=request.GET.get('res_id'))
    val = request.GET.get('value')
    if val == 'True':
        res.show_up = True
    else:
        res.show_up = False
    res.save()
    return HttpResponse('')
