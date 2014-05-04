from django.conf.urls import patterns, url

#from enarocanje.mynewsletter import views

urlpatterns = patterns(
    'enarocanje.mynewsletter.views',
    url(r'^mynewsletter$', 'newsletter', name='mynewsletter'),
    url(r'^mynewsletter/send$', 'send', name='sendnewsletter'),
)