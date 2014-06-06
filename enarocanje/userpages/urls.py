from django.conf.urls import patterns, url

urlpatterns = patterns('enarocanje.userpages.views',
                       url(r'^u/(?P<user_link>[A-Za-z0-9-_]+)$', 'userpage_main', name='userpage_main')
                       )
