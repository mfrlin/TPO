from django.conf.urls import patterns, url

urlpatterns = patterns('enarocanje.reservations',
	url(r'^myreservations$', 'views.myreservations', name='myreservations'),
	url(r'^myreservations/gcal/$', 'gcal.edit', name='gcal'),
	url(r'^myreservations/gcal/callback$', 'gcal.callback', name='gcalcallback'),

	url(r'^services/(?P<id>\d+)$', 'views.reservation', name='service'),
	url(r'^services/(?P<id>\d+)/reservation$', 'views.reservation', name='reservation'),
	url(r'^calendar.json$', 'rcalendar.calendarjson', name='calendarjson'),
)
