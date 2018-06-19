import json
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from friends.datapreprocessing import checkers
from core.models import Profile, Notification
from datainput.models import HealthCareWasteManagement, FamilyProfileLine, InformalSettlers, MaternalCare, Immunization, \
    Malaria, Tuberculosis, Schistosomiasis, Flariasis, Leprosy, ChildCare, STISurveillance, NutritionalStatus
from datapreprocessing.forms import MetricForm, EditMetricForm
from datapreprocessing.models import Metric, DataMap, RootCause
import operator
from friends import datapoints


@login_required
def index(request):

    if not checkers.is_updated():
        messages.error(request, 'Data is not yet up to date')
        return redirect('core:nutritionist')

    metrics = Metric.objects.filter(is_completed=False)

    profile = Profile.objects.get(user=request.user)

    context = {
        'profile': profile,
        'active': 'mt',
        'metrics': metrics,
        'date': datetime.now().date()
    }

    return render(request, 'datapreprocessing/index.html', context)


@login_required
def add_metric(request):

    form = MetricForm(request.POST or None)

    hcwm = HealthCareWasteManagement._meta.get_fields()[2:]
    family_profile = FamilyProfileLine._meta.get_fields()
    informal_settlers = InformalSettlers._meta.get_fields()[1:2]
    maternal = MaternalCare._meta.get_fields()[1:10]
    immunization = Immunization._meta.get_fields()[1:11]
    malaria = Malaria._meta.get_fields()[1:6]
    tb = Tuberculosis._meta.get_fields()[1:5]
    schisto = Schistosomiasis._meta.get_fields()[1:3]
    flariasis = Flariasis._meta.get_fields()[1:4]
    leprosy = Leprosy._meta.get_fields()[1:3]
    child_care = ChildCare._meta.get_fields()[1:13]
    sti = STISurveillance._meta.get_fields()[2:5]

    fp = operator.itemgetter(3, 4, 5, 6, 7, 11, 12, 13, 14, 15, 19, 20)

    profile = Profile.objects.get(user=request.user)

    context = {
        'profile': profile,
        'active': 'mt',
        'form': form,
        'hcwm': hcwm,
        'family_profile': fp(family_profile),
        'informal_settlers': informal_settlers,
        'maternal': maternal,
        'immunization': immunization,
        'malaria': malaria,
        'tb': tb,
        'schisto': schisto,
        'flariasis': flariasis,
        'leprosy': leprosy,
        'child_care': child_care,
        'educ': datapoints.educational_attainment,
        'toilet': datapoints.toilet_type,
        'water': datapoints.water_sources,
        'food': datapoints.food_production,
        'sti': sti,
        'nutritional_statuses': NutritionalStatus.objects.all()
    }

    if form.is_valid():

        f = form.save(commit=False)
        f.metric = request.POST.get('metric')
        f.save()

        messages.success(request, 'Metric added successfully')
        return redirect('datapreprocessing:index')

    return render(request, 'datapreprocessing/add_metric.html', context)


@login_required
def delete_metric(request, id):

    Metric.objects.get(id=id).delete()

    messages.success(request, 'Metric deleted successfully')
    return redirect('datapreprocessing:index')


@login_required
def edit_metric(request, id):

    metric = Metric.objects.get(id=id)

    form = EditMetricForm(request.POST or None, instance=metric)

    if form.is_valid():
        f = form.save(commit=False)
        f.metric = metric.metric
        f.save()

        messages.success(request, 'Threshold successfully edited')
        return redirect('datapreprocessing:index')

    profile = Profile.objects.get(user=request.user)

    context = {
        'profile': profile,
        'active': 'mt',
        'form': form,
        'metric': metric.metric
    }

    return render(request, 'datapreprocessing/edit_metric.html', context)


class DataMap(View):
    @staticmethod
    @login_required
    def get(request):
        context = {
            'metrics': Metric.objects.all()
        }
        return render(request, 'datapreprocessing/add_root_cause.html', context)

    @staticmethod
    @login_required
    def post(request):
        # new_root_cause = RootCause.objects.create(name=request.POST.get('root_cause'))
        new_root_cause = RootCause(name=request.POST['root_cause'])
        print(new_root_cause)
        new_root_cause.save()

        print(new_root_cause)

        metric = Metric.objects.get(metric=request.POST.get('metric'))
        DataMap.objects.create(root_cause=new_root_cause, metric=metric)

        data = {
            "new_root_cause": new_root_cause.name
        }
        return JsonResponse(data)

