import datetime
import json

from django.http import Http404, HttpResponse
from django.utils.translation import ugettext_lazy as _, ugettext

from enarocanje.service.models import Service
from enarocanje.accountext.models import ServiceProvider
from enarocanje.reservations.models import Reservation
from enarocanje.workinghours.models import Absence, WorkingHours, EmployeeWorkingHours
from enarocanje.employees.models import Employee

EVENT_TITLE_CLOSED = _('Closed')
EVENT_TITLE_CLOSED_WHOLE_DAY = _('Closed on this day')
EVENT_TITLE_NOT_WORKING = _('Employee absent')
EVENT_TITLE_NOT_WORKING_WHOLE_DAY = _("Doesn't work")
EVENT_TITLE_RESERVED = _('Reserved')

EVENT_CLOSED_COLOR = '#E02D2D'
EVENT_PAUSE_COLOR = '#CCCCCC'
EVENT_RESERVED_COLOR = '#FF8000'


def calendarjson(request):
    try:
        provider = ServiceProvider.objects.get(id=request.GET.get('service_provider_id'))
        service = Service.objects.get(id=request.GET.get('service_id'))
        start = datetime.datetime.fromtimestamp(int(request.GET.get('start')))
        end = datetime.datetime.fromtimestamp(int(request.GET.get('end')))
    except:
        raise Http404
    return HttpResponse(json.dumps(getEvents(service, provider, start, end)))


def reservations_calendar(request):
    try:
        provider = ServiceProvider.objects.get(id=request.GET.get('service_provider_id'))
        start = datetime.datetime.fromtimestamp(int(request.GET.get('start')))
        end = datetime.datetime.fromtimestamp(int(request.GET.get('end')))
    except:
        raise Http404
    return HttpResponse(json.dumps(get_all_reservations(None, provider, start, end)))


def encodeDatetime(dt):
    if isinstance(dt, datetime.date):
        return dt.isoformat()
    elif isinstance(dt, datetime.datetime):
        return dt.isoformat('T') + 'Z'
    else:
        raise Exception()


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


def getMinMaxTime(provider):
    workinghours = list(provider.working_hours.all())
    if not workinghours:
        return None, None
    return min(wh.time_from for wh in workinghours), max(wh.time_to for wh in workinghours)


def getEvents(service, provider, start, end):
    events = []

    for date in daterange(start.date(), end.date()):
        start = datetime.datetime.combine(date, datetime.time(0))
        end = datetime.datetime.combine(date + datetime.timedelta(days=1), datetime.time(0))
        events.extend(getReservations(service, provider, start, end))
        events.extend(getWorkingHours(service, provider, date, True))

    return events


def getReservations(service, provider, start, end):
    events = []
    working_employees = []
    if service.employees.all():
        for emp in service.employees.all():
            if EmployeeWorkingHours.get_for_day(emp, start.date().weekday()) is not None:
                working_employees.append(emp)
        today_res = Reservation.objects.filter(date__gte=start, date__lt=end)
        if list(service.employees.all()).__len__() > 1:
            today_res = today_res.filter(employee__in=working_employees)
        active_during_termin = dict()
        for r in today_res:
            start = datetime.datetime.combine(start.date(), r.time)
            end = start + datetime.timedelta(minutes=r.service_duration)
            while start < end:
                if r.active_during(start):
                    if not start in active_during_termin:
                        active_during_termin[start] = 1
                    else:
                        active_during_termin[start] += 1

                start += datetime.timedelta(minutes=15)

        overlaps = []
        currently_working = working_employees
        for term in active_during_termin.keys():
            cur_emp = list(working_employees).__len__()
            for emp in currently_working:
                cwh = EmployeeWorkingHours.get_for_day(emp, start.weekday())
                if term + datetime.timedelta(minutes=service.duration) > datetime.datetime.combine(start.date(),
                                                                                                   cwh.time_to):
                    cur_emp -= 1

            if active_during_termin[term] >= cur_emp:
                overlaps.append(term)

        if overlaps:
            events.extend(group_events(overlaps))
    else:
        events.extend(get_all_reservations(service, provider, start, end))

    return events


def getWorkingHours(service, provider, date, past):
    workinghrs = WorkingHours.get_for_day(provider, date.weekday())
    events = []

    if past:
        now = datetime.datetime.now()
        if date < now.date():
            return [
                {
                    'title': ugettext('In the past'),
                    'start': encodeDatetime(date),
                    'end': encodeDatetime(datetime.datetime.combine(date, datetime.time(23, 59))),
                    'color': '#444444'
                }
            ]
        elif date == now.date():
            events.append(
                {
                    'title': ugettext('In the past'),
                    'start': encodeDatetime(date),
                    'end': encodeDatetime(datetime.datetime.combine(date, now.time())),
                    'color': '#444444'
                }
            )

    # Check if provider is working on this date
    if workinghrs is None or Absence.is_absent_on(provider, date):
        return [
            {
                'title': ugettext(EVENT_TITLE_CLOSED_WHOLE_DAY),
                'start': encodeDatetime(date),
                'end': encodeDatetime(date + datetime.timedelta(days=1)),
                'color': EVENT_CLOSED_COLOR
            }
        ]

    # Start
    events.append({
        'title': ugettext(EVENT_TITLE_CLOSED),
        'start': encodeDatetime(date),
        'end': encodeDatetime(datetime.datetime.combine(date, workinghrs.time_from)),
        'color': EVENT_PAUSE_COLOR
    })

    # End
    events.append({
        'title': ugettext(EVENT_TITLE_CLOSED),
        'start': encodeDatetime(datetime.datetime.combine(date, workinghrs.time_to)),
        'end': encodeDatetime(date + datetime.timedelta(days=1)),
        'color': EVENT_PAUSE_COLOR
    })

    for wrkbrk in workinghrs.breaks.all():
        events.append({
            'title': ugettext(EVENT_TITLE_CLOSED),
            'start': encodeDatetime(datetime.datetime.combine(date, wrkbrk.time_from)),
            'end': encodeDatetime(datetime.datetime.combine(date, wrkbrk.time_to)),
            'color': EVENT_PAUSE_COLOR
        })

    if service is not None:
        employees = Employee.objects.filter(id__in=service.employees.all(), employer=provider.id)
    else:
        employees = Employee.objects.filter(employer=provider.id).all()
    first_arrive = datetime.time(23, 59)
    last_gone = datetime.time(0)
    for e in employees:
        if e.working_hours.all():
            cwh = e.working_hours.all()[0].get_for_day(e, date.weekday())
        if cwh:
            if cwh.time_to > last_gone:
                last_gone = cwh.time_to
            if cwh.time_from < first_arrive:
                first_arrive = cwh.time_from
    if employees:
        if first_arrive == datetime.time(23, 59) and last_gone == datetime.time(0):
            return [{
                        'title': ugettext('No employees scheduled but we are still open. Huh.'),
                        'start': encodeDatetime(date),
                        'end': encodeDatetime(date + datetime.timedelta(days=1)),
                        'color': EVENT_CLOSED_COLOR
                    }]
        else:
            if first_arrive > workinghrs.time_from:
                events.append({
                    'title': ugettext('No employees here yet'),
                    'start': encodeDatetime(datetime.datetime.combine(date, workinghrs.time_from)),
                    'end': encodeDatetime(datetime.datetime.combine(date, first_arrive)),
                    'color': EVENT_PAUSE_COLOR
                })
            if last_gone < workinghrs.time_to:
                events.append({
                    'title': ugettext('All employees have left'),
                    'start': encodeDatetime(datetime.datetime.combine(date, last_gone)),
                    'end': encodeDatetime(datetime.datetime.combine(date, workinghrs.time_to)),
                    'color': EVENT_PAUSE_COLOR
                })
    return events


# for employees

def getEmployeeTimetable(request):
    service = None
    emp = None
    sp_id = request.GET.get('service_provider_id')
    sp = ServiceProvider.objects.get(id=sp_id)
    emp_id = request.GET.get('employee_id')
    if emp_id:
        emp = Employee.objects.get(id=emp_id)
    s_id = request.GET.get('service_id')
    if s_id:
        service = Service.objects.get(id=s_id)

    start = datetime.datetime.fromtimestamp(int(request.GET.get('start')))
    end = datetime.datetime.fromtimestamp(int(request.GET.get('end')))

    if not emp_id and not s_id:
        return HttpResponse(json.dumps(get_all_reservations(None, sp, start, end)))
    if s_id and not emp_id:
        return getServiceEvents(service, sp, start, end)

    past = True
    if request.GET.get('past') == 'true':
        past = False

    return HttpResponse(json.dumps(getEmpEvents(sp, emp, service, start, end, past)))


def getServiceEvents(service, provider, start, end):
    events = []
    reservations = Reservation.objects.filter(service=service, date__gte=start, date__lte=end)

    for date in daterange(start.date(), end.date()):
        events.extend(getWorkingHours(service, provider, date, False))

    for reservation in reservations:
        text = EVENT_TITLE_RESERVED
        if reservation.employee:
            text += _(' at ') + reservation.employee.__unicode__()
        dt = datetime.datetime.combine(reservation.date, reservation.time)
        events.append({
            'title': ugettext(text),
            'start': encodeDatetime(dt),
            'end': encodeDatetime(dt + datetime.timedelta(minutes=reservation.service_duration)),
            'color': EVENT_RESERVED_COLOR
        })
    return HttpResponse(json.dumps(events))


def getEmpEvents(provider, employee, service, start, end, past):
    events = []

    # Get reservation events
    events.extend(getEmployeeReservations(employee, service, start, end))

    # Get working hours events
    for date in daterange(start.date(), end.date()):
        events.extend(getEmployeeWorkingHours(provider, employee, date, past))
    return events


def getEmployeeReservations(employee, service, start, end):
    reservations = Reservation.objects.filter(employee=employee, date__gte=start, date__lte=end)
    if service:
        reservations = reservations.filter(service=service)

    events = []

    for reservation in reservations:
        dt = datetime.datetime.combine(reservation.date, reservation.time)
        events.append({
            'title': ugettext(EVENT_TITLE_RESERVED),
            'start': encodeDatetime(dt),
            'end': encodeDatetime(dt + datetime.timedelta(minutes=reservation.service_duration)),
            'color': EVENT_RESERVED_COLOR
        })
    return events


def getEmployeeWorkingHours(provider, employee, date, past):
    sp_workinghrs = WorkingHours.get_for_day(provider, date.weekday())
    workinghrs = EmployeeWorkingHours.get_for_day(employee, date.weekday())
    events = []

    if past:
        now = datetime.datetime.now()
        if date < now.date():
            return [
                {
                    'title': ugettext('In the past'),
                    'start': encodeDatetime(date),
                    'end': encodeDatetime(datetime.datetime.combine(date, datetime.time(23, 59))),
                    'color': '#444444'
                }
            ]
        elif date == now.date():
            events.append(
                {
                    'title': ugettext('In the past'),
                    'start': encodeDatetime(date),
                    'end': encodeDatetime(datetime.datetime.combine(date, now.time())),
                    'color': '#444444'
                }
            )

    # TODO add employee absence support
    if sp_workinghrs is None or Absence.is_absent_on(provider, date):
        return [
            {
                'title': ugettext(EVENT_TITLE_CLOSED_WHOLE_DAY),
                'start': encodeDatetime(date),
                'end': encodeDatetime(date + datetime.timedelta(days=1)),
                'color': EVENT_CLOSED_COLOR
            }
        ]
    if workinghrs is None:
        return [
            {
                'title': ugettext(EVENT_TITLE_NOT_WORKING_WHOLE_DAY),
                'start': encodeDatetime(date),
                'end': encodeDatetime(date + datetime.timedelta(days=1)),
                'color': EVENT_CLOSED_COLOR
            }
        ]

    events.append({
        'title': ugettext(EVENT_TITLE_NOT_WORKING),
        'start': encodeDatetime(date),
        'end': encodeDatetime(datetime.datetime.combine(date, workinghrs.time_from)),
        'color': EVENT_PAUSE_COLOR
    })

    events.append({
        'title': ugettext(EVENT_TITLE_NOT_WORKING),
        'start': encodeDatetime(datetime.datetime.combine(date, workinghrs.time_to)),
        'end': encodeDatetime(date + datetime.timedelta(days=1)),
        'color': EVENT_PAUSE_COLOR
    })

    for wrkbrk in sp_workinghrs.breaks.all():
        events.append({
            'title': ugettext(EVENT_TITLE_CLOSED),
            'start': encodeDatetime(datetime.datetime.combine(date, wrkbrk.time_from)),
            'end': encodeDatetime(datetime.datetime.combine(date, wrkbrk.time_to)),
            'color': EVENT_PAUSE_COLOR
        })

    return events


def get_all_reservations(service, provider, start, end):
    events = []

    for date in daterange(start.date(), end.date()):
        events.extend(getWorkingHours(service, provider, date, False))

    today_res = Reservation.objects.filter(date__gte=start, date__lt=end, service_provider=provider)
    for reservation in today_res:
        dt = datetime.datetime.combine(reservation.date, reservation.time)
        text = EVENT_TITLE_RESERVED
        if reservation.employee:
            text += _(' at ') + reservation.employee.__unicode__()
        events.append({
            'title': ugettext(text),
            #'url': '/',
            'start': encodeDatetime(dt),
            'end': encodeDatetime(dt + datetime.timedelta(minutes=reservation.service_duration)),
            'color': EVENT_RESERVED_COLOR
        })
    return events


def group_events(ls):
    ls.sort()
    groups = []
    start = ls[0]
    cur = start
    cur_event = dict({'start': encodeDatetime(start), 'end': encodeDatetime(start + datetime.timedelta(minutes=15)),
                      'title': ugettext(EVENT_TITLE_RESERVED), 'color': EVENT_RESERVED_COLOR})
    ls.remove(start)
    i = 0
    length = ls.__len__()
    while i <= length:
        end = cur + datetime.timedelta(minutes=15)
        if end in ls:
            ls.remove(end)
            cur_event['end'] = encodeDatetime(end + datetime.timedelta(minutes=15))
            cur = end
        else:
            if ls:
                cur = end + datetime.timedelta(minutes=15)
                while cur not in ls:
                    cur = cur + datetime.timedelta(minutes=15)
                groups.append(cur_event)
                cur_event = dict({'title': ugettext(EVENT_TITLE_RESERVED), 'color': EVENT_RESERVED_COLOR})
                cur_event['start'] = encodeDatetime(cur)
                cur_event['end'] = encodeDatetime(cur + datetime.timedelta(minutes=15))
                i += 1
        i += 1

    groups.append(cur_event)
    return groups


def getEmployeeDesc(request):
    try:
        employee = Employee.objects.get(id=request.GET.get('employee_id'))
    except:
        raise Http404
    if employee.description is not None:
        return HttpResponse(employee.description)
    else:
        return HttpResponse('')


def findEventByColor(events, color):
    for l in events:
        if l['color'] == color:
            return l
        else:
            return None


def getEmployeesForService(request):
    if not request.GET.get('service_id'):
        return HttpResponse(json.dumps([]))
    service_id = request.GET.get('service_id')
    service = Service.objects.get(id=service_id)
    employees = Employee.objects.filter(id__in=service.employees.all()).values_list('id', flat=True)
    return HttpResponse(json.dumps(list(employees)))


def getServicesForEmployee(request):
    emp_id = request.GET.get('employee_id')
    services = Service.objects.filter(employees__in=emp_id).values_list('id', flat=True)
    return HttpResponse(json.dumps(list(services)))