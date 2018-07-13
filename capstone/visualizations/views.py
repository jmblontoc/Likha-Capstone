import decimal
import json

from django.contrib import messages
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
# Create your views here.
from datainput.models import NutritionalStatus, Sex, MaternalCare, ChildCare, FHSIS
from friends.datamining.correlations import get_weight_values_per_month


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

    }

    return render(request, 'visualizations/insights/nutritional_status.html', context)


@login_required
def city_micronutrient(request):

    context = {

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


