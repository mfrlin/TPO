from django.core.urlresolvers import reverse
from django.views.generic import UpdateView, CreateView, ListView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from .models import Customer
from .forms import CustomerForm
from enarocanje.accountext.decorators import for_service_providers
from enarocanje.reservations.models import Reservation

from django.db.models import Q


class ListCustomerView(ListView):
    model = Customer
    template_name = 'customer_list.html'

    def get_queryset(self):
        provider = self.request.user.service_provider
        sort_by = self.request.GET.get('sort_by', 'name')
        search_by = self.request.GET.get('search_by', '')
        name = Q(name__regex=search_by)
        email = Q(email__regex=search_by)
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


class ListCustomerReservations(ListView):
    model = Reservation
    template_name = 'customers/reservations_list.html'

    def get_queryset(self):
        try:
            print(self.request.GET)
            user = Customer.objects.get(pk=self.kwargs.get('pk', -1)).user
        except:
            user = -1
        return Reservation.objects.filter(user=user, service_provider=self.request.user.service_provider)

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
