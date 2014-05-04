from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^accounts/signup/$', 'enarocanje.accountext.views.signup'),
                       url(r'^accounts/profile/$', 'enarocanje.accountext.views.account_profile',
                           name='account_profile'),
                       url(r'^cookies/', 'enarocanje.views.cookies'),
                       url(r'^', include('enarocanje.service.urls')),
                       url(r'^', include('enarocanje.workinghours.urls')),
                       url(r'^', include('enarocanje.reservations.urls')),
                       url(r'^', include('enarocanje.coupon.urls')),
<<<<<<< HEAD
                       url(r'^', include('enarocanje.mynewsletter.urls')),
=======
                       url(r'^', include('enarocanje.customers.urls')),

>>>>>>> 9e7fc42d9af98e042c163d447e95e45d57348a04

                       # External apps
                       url(r'^accounts/', include('allauth.urls')),

                       # Django admin
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
