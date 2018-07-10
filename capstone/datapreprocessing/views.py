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
from datapreprocessing.models import Metric
import operator
from friends import datapoints
from friends.datainput import validations


@login_required
def index(request):

    if len(validations.todo_list()) > 0:
        messages.error(request, 'Data is not yet up to date')
        return redirect('core:nutritionist')

    metrics = Metric.objects.filter(is_completed=False)

    profile = Profile.objects.get(user=request.user)

    context = {
        'profile': profile,
        'active': 'mt',
        'metrics': metrics,
        'date': datetime.now().date(),
        'has_nutritional': checkers.has_nutritional(),
        'has_micronutrient': checkers.has_micronutrient(),
        'has_maternal': checkers.has_maternal(),
        'has_child_care': checkers.has_child_care(),
        'has_socioeconomic': checkers.has_socioeconomic()
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


@login_required
def set_nutritional_status(request):

    if request.method == 'GET':

        context = {
            'nutritional_statuses': NutritionalStatus.objects.all()
        }

        return render(request, 'datapreprocessing/default_metrics/nutritional_status.html', context)

    else:

        my_dict = dict(request.POST)

        for k, v in my_dict.items():

            if k != 'csrfmiddlewaretoken':

                value = v[0]
                model = 'Nutritional Status'
                status = NutritionalStatus.objects.get(code=k)

                metric = '%s | %s' % (model, status.name)
                Metric.objects.create(
                    metric=metric,
                    threshold=value,
                    unit='Total',
                )

        messages.success(request, 'Thresholds successfully set')
        return redirect('datapreprocessing:index')


@login_required
def set_micronutrient(request):

    if request.method == 'GET':

        context = {
            'fields': datapoints.micronutrient
        }

        return render(request, 'datapreprocessing/default_metrics/micronutrient.html', context)

    if request.method == 'POST':

        my_dict = dict(request.POST)

        print(my_dict)

        for k, v in my_dict.items():

            counter = 0

            if not k == 'csrfmiddlewaretoken' and not k == 'is_bad':

                value = v[0]
                model = 'Child Care'
                field = k

                metric = '%s | %s' % (model, field)

                Metric.objects.create(
                    metric=metric,
                    threshold=value,
                    unit='Total'
                )

            counter = counter + 1

        messages.success(request, 'Thresholds successfully set')
        return redirect('datapreprocessing:index')


@login_required
def set_maternal(request):

    if request.method == 'GET':

        context = {
            'fields': datapoints.maternal
        }

        return render(request, 'datapreprocessing/default_metrics/maternal.html', context)

    if request.method == 'POST':

        my_dict = dict(request.POST)

        for k, v in my_dict.items():

            if not k == 'csrfmiddlewaretoken':

                value = v[0]
                field = k
                metric = '%s | %s' % ('Maternal Care', field)

                Metric.objects.create(metric=metric, threshold=value, unit='Total')

        messages.success(request, 'Thresholds successfully set')
        return redirect('datapreprocessing:index')


@login_required
def set_child_care(request):

    if request.method == 'GET':

        context = {
            'fields': datapoints.child_care
        }

        return render(request, 'datapreprocessing/default_metrics/child_care.html', context)

    if request.method == 'POST':

        my_dict = dict(request.POST)

        for k, v in my_dict.items():

            if not k == 'csrfmiddlewaretoken':
                value = v[0]
                field = k
                metric = '%s | %s' % ('Child Care', field)

                Metric.objects.create(metric=metric, threshold=value, unit='Total')

        messages.success(request, 'Thresholds successfully set')
        return redirect('datapreprocessing:index')


@login_required
def set_socioeconomic(request):

    if request.method == 'GET':

        context = {
            'fields': datapoints.socioeconomic
        }

        return render(request, 'datapreprocessing/default_metrics/socioeconomic.html', context)

    if request.method == 'POST':

        my_dict = dict(request.POST)

        for k, v in my_dict.items():

            if not k == 'csrfmiddlewaretoken':
                value = v[0]
                field = k
                metric = '%s | %s' % ('Family Profile', field)

                Metric.objects.create(metric=metric, threshold=value, unit='Total')

        messages.success(request, 'Thresholds successfully set')
        return redirect('datapreprocessing:index')



# # # # # # # # # AJAX # # # # # # # # # #

def view_threshold(request):

    report = request.GET['report']
    metrics = Metric.objects.all()

    if report == 'ns':

        data = [metric.to_dict() for metric in metrics if NutritionalStatus.objects.filter(name=metric.get_data_point).count() > 0]
        return JsonResponse(data, safe=False)

    elif report == 'cc':

        data = [metric.to_dict() for metric in metrics if metric.get_data_point in datapoints.child_care]
        return JsonResponse(data, safe=False)

    elif report == 'maternal':

        data = [metric.to_dict() for metric in metrics if metric.get_data_point in datapoints.maternal]
        return JsonResponse(data, safe=False)

    elif report == 'socio':

        data = [metric.to_dict() for metric in metrics if metric.get_data_point in datapoints.socioeconomic]
        return JsonResponse(data, safe=False)

    elif report == 'micro':

        data = [metric.to_dict() for metric in metrics if metric.get_data_point in datapoints.micronutrient]
        print(datapoints.micronutrient)
        return JsonResponse(data, safe=False)



