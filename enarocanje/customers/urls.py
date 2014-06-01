from django.conf.urls import patterns, url
import views
from enarocanje.customers.views import managecustomer

urlpatterns = patterns('enarocanje.customers',
                       url(r'^mycustomers$', views.ListCustomerView.as_view(), name='mycustomers'),
                       url(r'^mycustomers/new$', views.CreateCustomerView.as_view(), name='customers-new'),
                       url(r'^mycustomers/(?P<pk>\d+)/edit$', views.EditCustomerView.as_view(), name='customers-edit'),
                       url(r'^mycustomers/(?P<pk>\d+)/reservations$', views.ListCustomerReservations.as_view(),
                           name='customers-reservations'),
                       url(r'^mycustomers/manage$', managecustomer, name='managecustomer'),
                       )
