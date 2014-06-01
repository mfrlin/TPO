from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.i18n import javascript_catalog

admin.autodiscover()

js_info_dict = {
    'packages': ('enarocanje.userpages.package', ),
}

urlpatterns = patterns('',
                       url(r'^accounts/signup/$', 'enarocanje.accountext.views.signup'),
                       url(r'^accounts/profile/$', 'enarocanje.accountext.views.account_profile',
                           name='account_profile'),
                       url(r'^cookies/', 'enarocanje.views.cookies'),
                       url(r'^', include('enarocanje.service.urls')),
                       url(r'^', include('enarocanje.workinghours.urls')),
                       url(r'^', include('enarocanje.reservations.urls')),
                       url(r'^', include('enarocanje.coupon.urls')),
                       url(r'^', include('enarocanje.employees.urls')),
                       
                       #banana
                       url(r'^', include('banana_py.urls')),

                       url(r'^', include('enarocanje.userpages.urls')),

                       url(r'^', include('enarocanje.mynewsletter.urls')),
                       url(r'^', include('enarocanje.customers.urls')),

                       url(r'^jsi18n/$', javascript_catalog, js_info_dict),

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
