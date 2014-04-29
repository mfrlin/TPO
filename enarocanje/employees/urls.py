from django.conf.urls import patterns, url

urlpatterns = patterns('enarocanje.employees.views',
                       url(r'^myemployees/$', 'myemployees', name='myemployees'),
                       url(r'^myemployees/add$', 'add', name='addemployee'),
                       url(r'^myemployees/edit/(?P<id>\d+)$', 'edit', name='editemployee'),
                       url(r'^myemployees/manage$', 'manage', name='manageemployee'),
)

