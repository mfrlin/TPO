from django.conf.urls import patterns, url

urlpatterns = patterns('enarocanje.userpages.views',
                       url(r'^u/(?P<id>\d+)$', 'userpage_main', name='userpage_main')
)
