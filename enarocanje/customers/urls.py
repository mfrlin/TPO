from django.conf.urls import patterns, url
import views
from enarocanje.customers.views import managecustomer
from enarocanje.customers.views import export_customers

urlpatterns = patterns('enarocanje.customers',
                       url(r'^mycustomers$', views.ListCustomerView.as_view(), name='mycustomers'),
                       url(r'^mycustomers/new$', views.CreateCustomerView.as_view(), name='customers-new'),
                       url(r'^mycustomers/export$', export_customers, name='export_customers'),
                       url(r'^mycustomers/(?P<pk>\d+)/edit$', views.EditCustomerView.as_view(), name='customers-edit'),
                       url(r'^mycustomers/(?P<pk>\d+)/reservations$', views.ListCustomerReservations.as_view(), name='customers-reservations'),
                       url(r'^mycustomers/manage$', managecustomer, name='managecustomer'),
)
