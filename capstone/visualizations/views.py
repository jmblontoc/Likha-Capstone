import decimal
import json

import django
from django.contrib import messages
from django.db.models import Q, Sum
from decimal import Decimal
from core.context_processors import profile
from friends import datapoints
from capstone import settings
from datapreprocessing.models import Metric
from friends.visualizations import getters
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from friends.datamining import correlations
from core.models import Profile, Notification
from friends.datapreprocessing import consolidators
from computations import weights, child_care as cc, socioeconomic as soc, maternal as mt
# Create your views here.
from datainput.models import NutritionalStatus, Sex, MaternalCare, ChildCare, FHSIS, Barangay, FamilyProfileLine, \
    OPTValues
from friends.datamining.correlations import get_weight_values_per_month, year_now
from visualizations.models import Report


@login_required
def index(request):
    profile = Profile.objects.get(user=request.user)

    context = {
        'profile': profile,
        'active': 'rv',
    }

    return render(request, 'visualizations/select_report.html', context)


@login_required
def city_nutritional_status(request):

    context = {
        'total_per_category': weights.totals_per_category(),
        'highest_per_category': weights.highest_barangay_per_category(),
        'count_per_barangay': weights.count_per_barangay_per_category()
    }

    return render(request, 'visualizations/insights/nutritional_status.html', context)


@login_required
def city_micronutrient(request):

    context = {
        'totals': cc.given_totals(),
        'highest': cc.highest(0),
        'lowest': cc.highest(123),
        'micro_per_barangay': cc.micro_per_barangay()
    }

    return render(request, 'visualizations/insights/micronutrient.html', context)


@login_required
def city_maternal(request):

    context = {

    }

    return render(request, 'visualizations/insights/maternal.html', context)


@login_required
def city_children_care(request):

    context = {

    }

    return render(request, 'visualizations/insights/children_care.html', context)

# # # # # # # # # # # # # # #


@login_required
def display_report(request):

    start_date = request.POST.get('date1')
    end_date = request.POST.get('date2')
    report = int(request.POST.get('report'))

    if start_date == '' or end_date == '':
        messages.error(request, 'Please put a date')
        return redirect('visualizations:index')

    profile = Profile.objects.get(user=request.user)

    context = {
        'profile': profile,
        'active': 'rv',
        'start_date': start_date,
        'end_date': end_date
    }

    if report == 1:
        return render(request, 'visualizations/nutritional_status.html', context)

    elif report == 2:
        return render(request, 'visualizations/micronutrient.html', context)

    elif report == 3:
        return render(request, 'visualizations/maternal.html', context)

    elif report == 4:
        return render(request, 'visualizations/child_care.html', context)


@login_required
def nutritional_status_report(request):

    context = {}

    return render(request, 'visualizations/nutritional_status.html', context)


@login_required
def micronutrient_report(request):

    context = {}

    return render(request, 'visualizations/micronutrient.html', context)


@login_required
def maternal_report(request):

    context = {}

    return render(request, 'visualizations/maternal.html', context)


@login_required
def child_care(request):

    context = {}

    return render(request, 'visualizations/child_care.html', context)


# # # # # # # # # # # # AJAX # # # # # # # # # # # #


@login_required
def get_nutritional_status(request):

    statuses = NutritionalStatus.objects.all()

    statuses_str = []

    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    stat = request.POST.get('status')

    male = Sex.objects.get(name='Male')
    female = Sex.objects.get(name='Female')

    male_values = []
    female_values = []

    for s in statuses:

        if stat in s.name:

            eopt_male = consolidators.get_total_opt_date(s, male, start_date, end_date)
            mr_male = consolidators.get_reweighing_counts(str(s), male)

            eopt_female = consolidators.get_total_opt_date(s, female, start_date, end_date)
            mr_female = consolidators.get_reweighing_counts(str(s), female)


            male_values.append(
                int(eopt_male)
            )

            female_values.append(
                int(eopt_female)
            )

            print(eopt_male + eopt_female)

            statuses_str.append(s.name)

    metrics = Metric.get_nutritional_status_by_category(stat)
    thresholds = [m['threshold'] for m in metrics]
    values = [m['value'] for m in metrics]


    data = {
        'male': male_values,
        'female': female_values,
        'statuses': statuses_str,
        'thresholds': thresholds,
        'values': values
    }

    return JsonResponse(data)


@login_required
def get_micronutrient(request):

    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')

    date_range = [start_date, end_date]

    fields = datapoints.micronutrient
    thresholds = [x['threshold'] for x in Metric.get_micronutrient()]
    values = [x['value'] for x in Metric.get_micronutrient()]

    data = {
        'male': getters.get_micronutrient(Sex.objects.get(name='Male'), date_range),
        'female': getters.get_micronutrient(Sex.objects.get(name='Female'), date_range),
        'fields': fields,
        'thresholds': thresholds,
        'values': values
    }

    return JsonResponse(data)


@login_required
def get_maternal(request):

    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')

    date_range = [start_date, end_date]

    fields = [x.verbose_name for x in MaternalCare._meta.get_fields()[1:10]]
    values = [int(x) for x in getters.get_maternal(date_range)]

    metrics = Metric.get_maternal()

    f = datapoints.maternal
    thresholds = [m['threshold'] for m in metrics]
    v = [m['value'] for m in metrics]

    data = {
        'fields': f,
        'values': v,
        'thresholds': thresholds
    }

    return JsonResponse(data)


@login_required
def get_child_care(request):

    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')

    date_range = [start_date, end_date]

    fields = [x.verbose_name for x in ChildCare._meta.get_fields()[1:13]]
    values = [int(x) for x in getters.get_child_care(date_range)]

    metrics = Metric.get_child_care()

    f = datapoints.child_care
    thresholds = [m['threshold'] for m in metrics]
    values = [m['value'] for m in metrics]

    data = {
        'fields': f,
        'values': values,
        'thresholds': thresholds
    }

    return JsonResponse(data)


def get_highest_barangay(request):

    return JsonResponse(weights.highest_barangay_per_category_json())


def top3_barangay_mns(request):

    highest = cc.top3_barangays(1)
    lowest = cc.top3_barangays(0)

    return JsonResponse({
        'highest': highest,
        'lowest': lowest
    })


# # # # # # # # # # # # # # # # REPORTS # # # # # # # # # # # # # # # # #

def report1(request):  # nutritional status

    total_opt = OPTValues.objects.filter(opt__date__year=year_now)

    context = {
        'barangays': Barangay.objects.all().order_by('name'),
        'families': FamilyProfileLine.objects.filter(family_profile__date__year=year_now).count(),
        'total_weighted': total_opt.aggregate(sum=Sum('values'))['sum'],
        'count011': total_opt.filter(Q(age_group__code='05') | Q(age_group__code='611')).aggregate(sum=Sum('values'))[
            'sum'],
        'count1271': total_opt.aggregate(sum=Sum('values'))['sum'] -
                    total_opt.filter(Q(age_group__code='05') | Q(age_group__code='611')).aggregate(sum=Sum('values'))[
                         'sum'],

        'wfa': weights.report_table()[0],
        'hfa': weights.report_table()[1],
        'wfh': weights.report_table()[2]
    }

    if request.method == 'GET':

        return render(request, 'visualizations/reports/nutritional_status.html', context)

    if request.method == 'POST':

        comment = request.POST['comment']
        json_data = str(serialize(context))

        Report.objects.create(
            name='City Nutritional Status Report',
            comments=comment,
            generated_by=profile(request)['profile'],
            json_data=json_data
        )

        messages.success(request, 'City Nutritional Status Report saved')
        return redirect('visualizations:reports_facility')


# socioeconomic
def report2(request):

    context = {
        'data': soc.report_table()
    }

    if request.method == 'GET':
        return render(request, 'visualizations/reports/socioeconomic.html', context)

    if request.method == 'POST':

        comment = request.POST['comment']
        json_data = str(serialize(context))

        Report.objects.create(
            name='Socioeconomic Status Report',
            comments=comment,
            generated_by=profile(request)['profile'],
            json_data=json_data
        )

        messages.success(request, 'City Socioeconomic Status Report saved')
        return redirect('visualizations:reports_facility')


# micronutrient
def report3(request):

    context = {
        'data': cc.report_table_micro()
    }

    if request.method == 'GET':
        return render(request, 'visualizations/reports/micronutrient.html', context)

    if request.method == 'POST':

        comment = request.POST['comment']
        json_data = str(context)

        Report.objects.create(
            name='City Micronutrient Supplementation Report',
            comments=comment,
            generated_by=profile(request)['profile'],
            json_data=json_data
        )

        messages.success(request, 'City Micronutrient Supplementation Report saved')
        return redirect('visualizations:reports_facility')


# child care
def report4(request):

    context = {
        'data': cc.report_table_child_care()['child_care'],
        'immunization': cc.report_table_child_care()['immunizations'],
        'malaria': cc.report_table_child_care()['malaria'],
        'tuberculosis': cc.report_table_child_care()['tb'],

        'cc_fields': datapoints.child_care,
        'imm_fields': datapoints.immunizations,
        'malaria_fields': datapoints.malaria,
        'tb_fields': datapoints.tuberculosis
    }

    if request.method == 'GET':
        return render(request, 'visualizations/reports/child_care.html', context)

    if request.method == 'POST':

        comment = request.POST['comment']
        json_data = str(context)

        Report.objects.create(
            name='City Children Care Report',
            comments=comment,
            generated_by=profile(request)['profile'],
            json_data=json_data
        )

        messages.success(request, 'City Children Care Report saved')
        return redirect('visualizations:reports_facility')


# maternal
def report5(request):

    context = {
        'fields': datapoints.maternal,
        'data': mt.maternal_report()
    }

    if request.method == 'GET':
        return render(request, 'visualizations/reports/maternal.html', context)

    if request.method == 'POST':
        comment = request.POST['comment']
        json_data = str(context)

        Report.objects.create(
            name='City Maternal Care Report',
            comments=comment,
            generated_by=profile(request)['profile'],
            json_data=json_data
        )

        messages.success(request, 'City Maternal Care Report saved')
        return redirect('visualizations:reports_facility')


# REPORTS FACILITY

def reports_facility(request):

    context = {

    }

    return render(request, 'visualizations/reports_facility.html', context)


def serialize(context):

    for key, value in context.items():
        if type(value) is django.db.models.query.QuerySet:
            context[key] = serializers.serialize('json', value)

    return context


# REPORTS LIBRARY
def reports_library(request):

    context = {
        'report1': Report.objects.filter(name__contains='City Nutritional Status'),
        'report3': Report.objects.filter(name__contains='City Micronutrient'),
        'report2': Report.objects.filter(name__contains='Socioeconomic'),
        'report4': Report.objects.filter(name__contains='Children Care'),
        'report5': Report.objects.filter(name__contains='Maternal')
    }

    return render(request, 'visualizations/reports_library.html', context)


# SAVED
def saved_report1(request, year):

    report = Report.objects.get(name__contains='City Nutritional Status', date__year=year)
    json_data = eval(report.json_data)

    barangay_data = json.loads(json_data['barangays'])

    context = {
        'barangays_count': len(barangay_data),
        'data': json_data,
        'report': report
    }

    return render(request, 'visualizations/saved/nutritional_status.html', context)


def saved_report3(request, year):

    report = Report.objects.get(name__contains='City Micronutrient', date__year=year)
    json_data = eval(report.json_data)

    context = {
        'report': report,
        'data': json_data
    }

    return render(request, 'visualizations/saved/micronutrient.html', context)


def saved_report2(request, year):

    report = Report.objects.get(name__contains='Socioeconomic', date__year=year)
    json_data = eval(report.json_data)

    context = {
        'report': report,
        'data': json_data
    }

    return render(request, 'visualizations/saved/socioeconomic.html', context)


def saved_report4(request, year):

    report = Report.objects.get(name__contains='Children Care', date__year=year)
    json_data = eval(report.json_data)

    context = {
        'report': report,
        'data': json_data
    }

    return render(request, 'visualizations/saved/child_care.html', context)


def saved_report5(request, year):

    report = Report.objects.get(name__contains='Maternal', date__year=year)
    json_data = eval(report.json_data)

    context = {
        'report': report,
        'data': json_data
    }

    return render(request, 'visualizations/saved/maternal.html', context)
