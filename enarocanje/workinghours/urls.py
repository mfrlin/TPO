from django.conf.urls import patterns, url

urlpatterns = patterns('enarocanje.workinghours.views',
                       url(r'^myworkinghours/$', 'myworkinghours', name='myworkinghours'),
                       url(r'^myworkinghours/add$', 'add', name='addworkinghours'),
                       url(r'^myworkinghours/addemp/(?P<id>\d+)$', 'addemp', name='addempworkinghours'),
                       url(r'^myworkinghours/edit/(?P<id>\d+)$', 'edit', name='editworkinghours'),
                       url(r'^myworkinghours/manage$', 'manage', name='manageworkinghours'),
                       url(r'^myworkinghours/manageemp/(?P<emp_id>\d+)/(?P<wh_id>\d+)$', 'manageemp', name='manageempworkinghours'),

                       url(r'^myabsences/$', 'myabsences', name='myabsences'),
                       url(r'^myabsences/add$', 'addabsence', name='addabsence'),
                       url(r'^myabsences/edit/(?P<id>\d+)$', 'editabsence', name='editabsence'),
                       url(r'^myabsences/manage$', 'manageabsence', name='manageabsence'),
)
