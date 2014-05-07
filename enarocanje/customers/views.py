from django.core.urlresolvers import reverse
from django.views.generic import UpdateView, CreateView, ListView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from .models import Customer
from .forms import CustomerForm
from enarocanje.accountext.decorators import for_service_providers


class ListCustomerView(ListView):
    model = Customer
    template_name = 'customer_list.html'

    def get_queryset(self):
        provider = self.request.user.service_provider
        sort_by = self.request.GET.get('sort_by', 'name')
        search_by = self.request.GET.get('search_by', '')
        if search_by:
            query = Customer.objects.filter(service=provider, name__regex=search_by)
        else:
            query = Customer.objects.filter(service=provider)
        if sort_by == 'name':
            return query.extra(
                select={'lower_name': 'lower(name)'}).order_by('lower_name')
        else:
            return query.order_by('-last_reservation')





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
        print customer
        if request.POST.get('action') == 'delete':
            customer.delete()
    return HttpResponseRedirect(reverse('mycustomers'))
