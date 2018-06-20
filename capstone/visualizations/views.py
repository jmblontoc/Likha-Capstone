import decimal
import json
from friends.visualizations import getters
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from friends.datamining import correlations
from friends.datapreprocessing import consolidators
# Create your views here.
from datainput.models import NutritionalStatus, Sex, MaternalCare, ChildCare
from friends.datamining.correlations import get_weight_values_per_month


@login_required
def index(request):

    context = {

    }

    return render(request, 'visualizations/index.html', context)


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

    statuses_str = [s.name for s in statuses]

    context = {

    }

    male = Sex.objects.get(name='Male')
    female = Sex.objects.get(name='Female')

    male_values = []
    female_values = []

    for s in statuses:
        eopt_male = consolidators.get_total_opt(s, male)
        mr_male = consolidators.get_reweighing_counts(str(s), male)

        eopt_female = consolidators.get_total_opt(s, female)
        mr_female = consolidators.get_reweighing_counts(str(s), female)

        male_values.append(
            int(eopt_male + mr_male)
        )

        female_values.append(
            int(eopt_female + mr_female)
        )

    data = {
        'male': male_values,
        'female': female_values,
        'statuses': json.dumps(statuses_str)
    }

    return JsonResponse(data)


@login_required
def get_micronutrient(request):

    fields = [
        'Vitamin A', 'Iron', 'MNP', 'ORS', 'BCG', 'HEPA B1', 'PENTA', 'OPV', 'MCV', 'ROTA', 'PCV'
    ]

    data = {
        'male': getters.get_micronutrient(Sex.objects.get(name='Male')),
        'female': getters.get_micronutrient(Sex.objects.get(name='Female')),
        'fields': fields
    }

    return JsonResponse(data)


@login_required
def get_maternal(request):

    fields = [x.verbose_name for x in MaternalCare._meta.get_fields()[1:10]]
    values = [int(x) for x in getters.get_maternal()]

    data = {
        'fields': fields,
        'values': values
    }

    return JsonResponse(data)


@login_required
def get_child_care(request):

    fields = [x.verbose_name for x in ChildCare._meta.get_fields()[1:13]]
    values = [int(x) for x in getters.get_child_care()]

    data = {
        'fields': fields,
        'values': values
    }

    return JsonResponse(data)


