import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from friends.causalmodel import helper
# Create your views here.
from datapreprocessing.models import Metric
from causalmodel.models import RootCause, DataMap, Block, Child


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


@login_required
def create_causal_model(request):

    root_causes = RootCause.objects.all()

    context = {
        'root_causes': root_causes
    }

    return render(request, 'causalmodel/create_causal_model.html', context)


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

    Block.objects.create(
        root_cause=root_cause,
        name=root_cause.name,
    )

    return JsonResponse('success', safe=False)


def insert_blocks(request):

    blocks = json.loads(request.POST['blocks'])

    for block in blocks:

        b = Block()
        b.name = block['name']
        b.save()

        causes = helper.get_root_causes(block['rootCauses'])
        for cause in causes:
            b.root_causes_content.add(cause)


        if block['child'] is not None:
            for child in block['child']:

                bl = Block.objects.get(name=child['name'])
                c = Child(block=bl, parent=b)
                c.save()


