from django.conf.urls import patterns, url
import views

urlpatterns = patterns('enarocanje.customers',
                       url(r'^mycustomers$', views.ListCustomerView.as_view(), name='mycustomers'),
                       url(r'^mycustomers/new$', views.CreateCustomerView.as_view(), name='customers-new'),
                       url(r'^mycustomers/(?P<pk>\d+)/edit$', views.EditCustomerView.as_view(), name='customers-edit'),


)
