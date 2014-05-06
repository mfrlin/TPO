from django.conf.urls import patterns, url

urlpatterns = patterns('enarocanje.service.views',
                       url(r'^myservices/$', 'myservices', name='myservices'),
                       url(r'^myunconfirmedreservations/managereservation$', 'managereservation',
                           name='managereservation'),
                       url(r'^myunconfirmedreservations/managereservationall$', 'managereservationall',
                           name='managereservationall'),
                       url(r'^myunconfirmedreservations/$', 'myunconfirmedreservations',
                           name='myunconfirmedreservations'),
                       url(r'^myservices/add$', 'add', name='addservice'),
                       url(r'^myservices/manage$', 'manage', name='manageservice'),
                       url(r'^myservices/edit/(?P<id>\d+)$', 'edit', name='editservice'),

                       url(r'^$', 'browse_providers', name='browseproviders'),
                       url(r'^services/$', 'browse_services', name='browseservices'),
                       url(r'^services/(?P<id>\d+)/comments$', 'service_comments', name='servicecomments'),

                       url(r'^gallery/(?P<id>\d+)$', 'view_gallery', name='gallery'),
                       url(r'^gallery/(?P<id>\d+)/upload$', 'async_file_upload', name='async_file_upload'),
                       
                       
                       url(r'^subscribe/$', 'subscribe', name='subscribe'),
)
