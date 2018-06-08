from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from friends.datapreprocessing import checkers
from datainput.models import HealthCareWasteManagement, FamilyProfileLine, InformalSettlers
from datapreprocessing.forms import MetricForm
from datapreprocessing.models import Metric


@login_required
def index(request):

    if not checkers.is_updated():
        messages.error(request, 'Data is not yet up to date')
        return redirect('core:nutritionist')

    metrics = Metric.objects.filter(is_completed=False)

    context = {
        'metrics': metrics
    }

    return render(request, 'datapreprocessing/index.html', context)


@login_required
def add_metric(request):

    form = MetricForm(request.POST or None)

    hcwm = HealthCareWasteManagement._meta.get_fields()[2:]
    family_profile = FamilyProfileLine._meta.get_fields()[2:]
    informal_settlers = InformalSettlers._meta.get_fields()[1:2]

    context = {
        'form': form,
        'hcwm': hcwm,
        'family_profile': family_profile,
        'informal_settlers': informal_settlers
    }

    return render(request, 'datapreprocessing/add_metric.html', context)