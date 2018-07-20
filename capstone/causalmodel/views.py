import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from friends.causalmodel import helper
# Create your views here.
from datapreprocessing.models import Metric
from causalmodel.models import RootCause, DataMap, Block, Child, CausalModel
from friends.datamining.correlations import create_session, year_now
from friends.datapreprocessing import checkers
from friends.datamining import correlations
from friends.datainput import validations


@login_required
def index(request, year):

    models = CausalModel.objects.filter(date__year=year)


    context = {
        'causals': models,
        'year_get': year
    }

    return render(request, 'causalmodel/index.html', context)


@login_required
def details(request, id):

    causal = CausalModel.objects.get(id=id)

    context = {
        'causal': causal
    }

    return render(request, 'causalmodel/details.html', context)


@login_required
def root_causes(request):

    if validations.todo_list().__len__() == 0:

        causes = RootCause.objects.all()
        current_tree = CausalModel.objects.filter(date__year=year_now, is_approved=True)

        context = {
            'root_causes': causes,
            'current_tree': current_tree
        }

        return render(request, 'causalmodel/root_causes.html', context)

    messages.error(request, 'Data is not up to date')
    return redirect('core:nutritionist')


@login_required
def add_root_cause(request):

    context = {
        'metrics': Metric.get_alarming(),
    }

    return render(request, 'causalmodel/add_root_cause.html', context)


@login_required
def create_causal_model(request):

    root_causes = RootCause.objects.filter(date__year=year_now)

    if not root_causes:
        messages.error(request, 'Please add root causes first.')
        return redirect('causalmodel:rc_index')

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

    return JsonResponse('success', safe=False)


def insert_blocks(request):

    blocks = json.loads(request.POST['blocks'])

    causal_model = CausalModel()
    causal_model.save()

    for block in blocks:

        b = Block()
        b.root_cause = helper.set_root_cause(block['name'])
        b.name = block['name']
        b.causal_model = causal_model
        b.save()

        causes = helper.get_root_causes(block['rootCauses'])
        for cause in causes:
            b.root_causes_content.add(cause)


        if block['child'] is not None:

            for child in block['child']:

                bl = Block.objects.get(name=child['name'], causal_model=causal_model)
                c = Child(block=bl, parent=b)
                c.save()

    child_dict = [x.to_tree_dict() for x in Child.objects.all()]
    return JsonResponse(child_dict, safe=False)


def get_blocks(request):

    id = request.POST['id']
    causal = CausalModel.objects.get(id=id)

    q1 = Child.objects.filter(block__causal_model=causal)

    child_dict = [x.to_tree_dict() for x in q1]
    return JsonResponse(child_dict, safe=False)
