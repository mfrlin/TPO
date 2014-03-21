import datetime

from apiclient.discovery import build
from oauth2client import xsrfutil
from oauth2client.client import OAuth2WebServerFlow, FlowExchangeError
from oauth2client.django_orm import Storage
import httplib2
import pyrfc3339

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import F
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from enarocanje.accountext.decorators import for_service_providers
from enarocanje.common.timeutils import add_timezone, to_timezone
from forms import GCalSettings
from models import GCal, Reservation

@for_service_providers
def callback(request):
	"""Callback from Google OAuth2"""
	try:
		if not xsrfutil.validate_token(settings.SECRET_KEY, request.REQUEST['state'], request.user):
			return HttpResponseBadRequest()
		credential = FLOW.step2_exchange(request.REQUEST)
		storage = Storage(GCal, 'id', request.user.service_provider, 'credential')
		storage.put(credential)
	except FlowExchangeError:
		return HttpResponseRedirect(reverse('myreservations'))
	return HttpResponseRedirect(reverse(edit))

@for_service_providers
def edit(request):
	"""Edit GCal settings"""
	service_provider = request.user.service_provider
	service = get_gcal(service_provider)
	if not service:
		FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, request.user)
		authorize_url = FLOW.step1_get_authorize_url()
		return HttpResponseRedirect(authorize_url)

	calendars = get_all_items(service.calendarList().list)
	initial = {'calendar': service_provider.gcal_id}

	if request.method == 'POST':
		form = GCalSettings(request.POST, calendars=calendars, initial=initial)
		if form.is_valid():
			if service_provider.gcal_id and service_provider.gcal_id != form.cleaned_data['calendar']:
				# change in google calendar selection, need full resync
				service = get_gcal(service_provider)
				reset_sync(service_provider)
			service_provider.gcal_id = form.cleaned_data['calendar']
			if service_provider.gcal_id == 'None':
				service_provider.gcal_id = None
			if service_provider.gcal_id == 'new':
				calendar = service.calendars().insert(body={'summary': 'E-Narocanje'}).execute()
				service_provider.gcal_id = calendar['id']
			service_provider.save()
			sync(service_provider)
			return HttpResponseRedirect(reverse('myreservations'))
	else:
		form = GCalSettings(calendars=calendars, initial=initial)

	return render_to_response('reservations/gcal.html', locals(), context_instance=RequestContext(request))

def get_gcal(service_provider):
	"""Get gcal object and service"""
	storage = Storage(GCal, 'id', service_provider, 'credential')
	credential = storage.get()
	if credential is None or credential.invalid == True:
		return None

	http = httplib2.Http()
	http = credential.authorize(http)
	service = build(serviceName='calendar', version='v3', http=http, developerKey=settings.GOOGLE_API_KEY)

	return service

def get_all_items(req, *args, **kwargs):
	"""Get all items from a service using nextPageToken"""
	page_token = None
	while True:
		res = req(pageToken=page_token, *args, **kwargs).execute()
		if res.get('items'):
			for item in res['items']:
				yield item
		page_token = res.get('nextPageToken')
		if not page_token:
			break

def convert_to_gcal_event(reservation):
	"""Convert reservation to GCal event"""
	start = add_timezone(datetime.datetime.combine(reservation.date, reservation.time), reservation.service_provider.get_timezone())

	return {
		'summary': '%s (%s)' % (reservation.user_fullname, reservation.service_name),
		'location': reservation.service_provider.full_address(),
		'start': {
			'dateTime': start.isoformat('T'),
		},
		'end': {
			'dateTime': (start + datetime.timedelta(minutes=reservation.service_duration)).isoformat('T'),
		},
		'attendees': [
		],
	}

def sync(service_provider):
	"""Sync GCal for a service provider"""
	service = get_gcal(service_provider)
	if not service or not service_provider.gcal_id:
		return 0, 0, 0

	# New reservations
	counter_created = 0
	for reservation in service_provider.reservations.select_for_update().filter(gcalimported__isnull=True, isfromgcal=False):
		event = service.events().insert(calendarId=service_provider.gcal_id, body=convert_to_gcal_event(reservation)).execute()
		reservation.gcalid = event['id']
		reservation.gcalimported = F('updated')
		reservation.save()
		counter_created += 1

	# Updates
	counter_updated = 0
	for reservation in service_provider.reservations.select_for_update().filter(gcalimported__lt=F('updated'), isfromgcal=False):
		service.events().update(calendarId=service_provider.gcal_id, eventId=reservation.gcalid, body=convert_to_gcal_event(reservation)).execute()
		reservation.gcalimported = F('updated')
		reservation.save()
		counter_updated += 1

	# Imports
	counter_imported = 0
	extra = {}
	if service_provider.gcal_updated:
		extra['updatedMin'] = service_provider.gcal_updated.isoformat('T')
	for event in get_all_items(service.events().list, calendarId=service_provider.gcal_id, singleEvents=True, **extra):
		if event['status'] == 'cancelled':
			# don't delete enarocanje events
			Reservation.objects.filter(gcalid=event['id'], isfromgcal=True).delete()
		else:
			if 'start' not in event or 'end' not in event or 'summary' not in event or 'updated' not in event:
				continue

			if 'dateTime' in event['start']:
				start = to_timezone(pyrfc3339.parser.parse(event['start']['dateTime']), service_provider.get_timezone())
			elif 'date' in event['start']:
				start = datetime.datetime.strptime(event['start']['date'], '%Y-%m-%d')
			else:
				continue

			if 'dateTime' in event['end']:
				end = to_timezone(pyrfc3339.parser.parse(event['end']['dateTime']), service_provider.get_timezone())
			elif 'date' in event['end']:
				end = datetime.datetime.strptime(event['end']['date'], '%Y-%m-%d')
			else:
				continue

			fields = {
				'date': start.date(),
				'time': start.time(),
				'service_name': event['summary'],
				'service_duration': (end - start).total_seconds() // 60,
				'isfromgcal': True,
			}

			reservation, created = Reservation.objects.get_or_create(service_provider=service_provider, gcalid=event['id'], defaults=fields)
			if not created and reservation.isfromgcal:
				# update fields (if it was created, they are already set)
				# skip events created by this script
				for field in fields:
					setattr(reservation, field, fields[field])
				reservation.save()

			updated = pyrfc3339.parser.parse(event['updated'])
			if service_provider.gcal_updated is None or service_provider.gcal_updated < updated:
				service_provider.gcal_updated = updated

		counter_imported += 1
	service_provider.save()

	return counter_created, counter_updated, counter_imported

def reset_sync(service_provider):
	service = get_gcal(service_provider)
	if not service:
		return service_provider

	Reservation.objects.filter(service_provider=service_provider, isfromgcal=True).delete()
	for reservation in Reservation.objects.filter(service_provider=service_provider).select_for_update():
		if service:
			try:
				service.events().delete(calendarId=service_provider.gcal_id, eventId=reservation.gcalid).execute()
			except:
				pass
		reservation.gcalid = None
		reservation.gcalimported = None
		reservation.save()
	service_provider.gcal_updated = None
	service_provider.save()
	return service_provider

FLOW = OAuth2WebServerFlow(client_id=settings.GOOGLE_CLIENT_ID,
	client_secret=settings.GOOGLE_CLIENT_SECRET,
	scope='https://www.googleapis.com/auth/calendar',
	redirect_uri=settings.BASE_URL + '/myreservations/gcal/callback',
	access_type='offline',
	approval_prompt='force')
