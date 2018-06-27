import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


# Create your views here.
from datapreprocessing.models import Metric
from causalmodel.models import RootCause, DataMap


@login_required
def index(request):

    context = {

    }

    return render(request, 'causalmodel/index.html', context)


@login_required
def root_causes(request):

    causes = RootCause.objects.all()

    context = {
        'root_causes': causes
    }

    return render(request, 'causalmodel/root_causes.html', context)


@login_required
def add_root_cause(request):

    scores = request.session['scores']
    correlations = [x for x in scores if 1 >= abs(x['score']) >= 0.5]

    context = {
        'metrics': Metric.get_alarming(),
        'correlations': correlations
    }

    return render(request, 'causalmodel/add_root_cause.html', context)


# ajax
def insert_root_cause(request):

    root_cause = RootCause.objects.create(name=request.POST['name'])

    for x in json.loads(request.POST.get('metrics')):
        DataMap.objects.create(
            root_cause=root_cause,
            metric=x['name'],
            value=x['value'],
            threshold=x['threshold']
        )

    return JsonResponse('success', safe=False)