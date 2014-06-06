import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.utils.translation import ugettext_lazy as _

from enarocanje.accountext.decorators import for_service_providers
from forms import WorkingHoursForm, WorkingHoursFormSet, AbsenceForm, EmployeeWorkingHoursForm
from models import WorkingHours, Absence, Employee, EmployeeWorkingHours, WorkingHoursBreak, DAYS_OF_WEEK_DICT_INT

# Working hours


def convert_str_h_to_int(str_hour):
    blc = str_hour.split(':')
    return int(blc[0]) * 100 + int(blc[1])


def convert_time_block_h_to_int(blck):
    return convert_str_h_to_int(blck[0]), convert_str_h_to_int(blck[1])


def check_overlap((StartA, EndA), (StartB, EndB)):
    return (StartA <= EndB) and (EndA >= StartB)


@for_service_providers
def myworkinghours(request):
    days_of_week_dict_int = DAYS_OF_WEEK_DICT_INT

    error_msg = []

    if request.POST.get('action_type') == 'save':
        days_wbl = {}

        funct_error = False

        for key, name in days_of_week_dict_int.items():

            time_from = request.POST.getlist('time_from_' + str(key))
            time_to = request.POST.getlist('time_to_' + str(key))

            if len(time_from) != len(time_to):
                error_msg.append(_("Fatal error: got malformed data!"))

                funct_error = True
                break

            try:
                x_dummy = filter(lambda x: convert_str_h_to_int(x), time_from)
                x_dummy = filter(lambda x: convert_str_h_to_int(x), time_to)
            except:
                error_msg.append(_("Fatal error: got malformed data!"))

                funct_error = True
                break

            hour_blocks = sorted(filter(lambda x: x[0] or x[1], zip(time_from, time_to)), key=lambda x: x[0])

            bad_blocks = len(filter(lambda x: x[0] >= x[1], hour_blocks))

            if bad_blocks:
                funct_error = True
                break

            for i, blck in enumerate(hour_blocks):
                for j, blck2 in enumerate(hour_blocks):
                    if i == j:
                        continue
                    if check_overlap(blck, blck2):
                        funct_error = True
                        break

            if funct_error:
                error_msg.append(_("Fatal error: got malformed data, blocks are overlaping!"))
                break

            if len(hour_blocks):

                breaks = []
                working_hours = []

                for i in range(0, len(hour_blocks) - 1):
                    break_begin = hour_blocks[i][1]
                    break_end = hour_blocks[i + 1][0]

                    breaks.append((break_begin, break_end))

                working_hours = (hour_blocks[0][0], hour_blocks[-1][1])

                days_wbl[key] = (working_hours, breaks)

        if not funct_error:
            workinghours = request.user.service_provider.working_hours.all()
            for wh in workinghours:
                wh_breaks = WorkingHoursBreak.objects.filter(working_hours=wh)
                wh_breaks.delete()

            workinghours.delete()

            for key, value in days_wbl.items():
                working_hours, breaks = value

                wh_ent = WorkingHours()
                wh_ent.service_provider = request.user.service_provider
                wh_ent.time_from = working_hours[0]
                wh_ent.time_to = working_hours[1]
                wh_ent.week_days = str(key)

                wh_ent.save()

                for brk in breaks:
                    whb_ent = WorkingHoursBreak()
                    whb_ent.working_hours = wh_ent
                    whb_ent.time_from = brk[0]
                    whb_ent.time_to = brk[1]

                    whb_ent.save()

    ## VIEW
    ##################
    workinghours = request.user.service_provider.working_hours.all()

    wkdys = dict()
    wkdys[1] = set([])
    wkdys[2] = set([])
    wkdys[3] = set([])
    wkdys[4] = set([])
    wkdys[5] = set([])
    wkdys[6] = set([])
    wkdys[7] = set([])

    for wh in workinghours:
        wh_breaks = WorkingHoursBreak.objects.filter(working_hours=wh)

        for week_day in map(int, wh.week_days_list()):
            wkdys[week_day].add(wh.time_from)
            wkdys[week_day].add(wh.time_to)

            for wh_b in wh_breaks:
                wkdys[week_day].add(wh_b.time_from)
                wkdys[week_day].add(wh_b.time_to)

    working_hours_blocks = {}
    for k, v in wkdys.iteritems():
        tuples = []
        v = sorted(list(v))
        for i in range(0, len(v), 2):
            tuples.append((v[i], v[i + 1]))

        working_hours_blocks[k] = tuples

    return render_to_response('workinghours/myworkinghours.html', locals(), context_instance=RequestContext(request))


@for_service_providers
def manage(request):
    if request.method == 'POST':
        workinghours = get_object_or_404(WorkingHours, service_provider=request.user.service_provider,
                                         id=request.POST.get('workinghours'))
        if request.POST.get('action') == 'delete':
            workinghours.delete()
    return HttpResponseRedirect(reverse(myworkinghours))

# Absences


@for_service_providers
def myabsences(request):
    absences = request.user.service_provider.absence_set.filter(date_to__gte=datetime.datetime.today())
    return render_to_response('workinghours/myabsences.html', locals(), context_instance=RequestContext(request))


@for_service_providers
def addabsence(request):
    if request.method == 'POST':
        form = AbsenceForm(request.POST)
        if form.is_valid():
            absence = form.save(commit=False)
            absence.service_provider = request.user.service_provider
            absence.save()
            return HttpResponseRedirect(reverse(myabsences))
    else:
        form = AbsenceForm()
    return render_to_response('workinghours/addabsence.html', locals(), context_instance=RequestContext(request))


@for_service_providers
def editabsence(request, id):
    absence = get_object_or_404(Absence, service_provider=request.user.service_provider, id=id)
    if request.method == 'POST':
        form = AbsenceForm(request.POST, instance=absence)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(myabsences))
    else:
        form = AbsenceForm(instance=absence)
    return render_to_response('workinghours/editabsence.html', locals(), context_instance=RequestContext(request))


@for_service_providers
def manageabsence(request):
    if request.method == 'POST':
        absence = get_object_or_404(Absence, service_provider=request.user.service_provider,
                                    id=request.POST.get('absence'))
        if request.POST.get('action') == 'delete':
            absence.delete()
    return HttpResponseRedirect(reverse(myabsences))


def addemp(request, id):
    emp = Employee.objects.get(id=id)
    if request.method == 'POST':
        form = EmployeeWorkingHoursForm(request.POST, employee=emp)
        valid = form.is_valid()
        if valid:
            wh = form.save(commit=False)
            wh.employee = emp
            wh.save()
            path = '/myemployees/edit/' + id
            return HttpResponseRedirect(path)
    else:
        initial = {}
        if not EmployeeWorkingHours.objects.filter(employee=emp).exists():
            initial['week_days'] = '1,2,3,4,5'
        else:
            t = EmployeeWorkingHours.objects.filter(employee=emp)
            #initial['week_days'] = t[0].week_days
            #initial['time_from'] = t[0].time_from
            #initial['time_to'] = t[0].time_to
        form = EmployeeWorkingHoursForm(initial=initial, employee=emp)
    return render_to_response('workinghours/addemp.html', locals(), context_instance=RequestContext(request))