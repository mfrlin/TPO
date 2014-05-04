from django.core.urlresolvers import reverse
from django.views.generic import UpdateView, CreateView, ListView

from .models import Customer
from .forms import CustomerForm


class ListCustomerView(ListView):
    model = Customer
    template_name = 'customer_list.html'

    def get_queryset(self):
        provider = self.request.user.service_provider
        sort_by = self.kwargs.get('sort_by', 'name')
        if sort_by == 'name':
            return Customer.objects.filter(service=provider).order_by('-name')
        else:
            return Customer.objects.filter(service=provider).order_by('last_reserved')


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
