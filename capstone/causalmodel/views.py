import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from capstone.decorators import not_bns, is_program_coordinator
from core.context_processors import get_user_type, profile
from core.models import Profile, Notification
from friends.causalmodel import helper
# Create your views here.
from datapreprocessing.models import Metric
from causalmodel.models import RootCause, DataMap, Block, Child, CausalModel, CausalModelComment
from friends.datamining.correlations import create_session, year_now
from friends.datapreprocessing import checkers
from friends.datamining import correlations
from friends.datainput import validations


@login_required
@not_bns
def index(request, year):

    profile = Profile.objects.get(user=request.user)

    if profile.user_type == 'Nutritionist':
        layout = 'core/nutritionist-layout.html'
    else:
        layout = 'core/pc_layout.html'

    models = CausalModel.objects.filter(date__year=year).order_by('-date')
    current_tree = CausalModel.objects.filter(date__year=year_now, is_approved=True)

    context = {
        'active': 'cm',
        'causals': models,
        'year_get': year,
        'current': current_tree,
        'layout': layout
    }

    return render(request, 'causalmodel/index.html', context)


@login_required
@not_bns
def details(request, id):

    causal = CausalModel.objects.get(id=id)

    context = {
        'causal': causal
    }

    return render(request, 'causalmodel/details.html', context)


@login_required
@not_bns
def root_causes(request):

    if validations.todo_list().__len__() == 0:

        causes = RootCause.objects.all()
        current_tree = CausalModel.objects.filter(date__year=year_now, is_approved=True)
        profile = Profile.objects.get(user=request.user)

        if profile.user_type == 'Nutritionist':
            template_values = 'core/nutritionist-layout.html'
        else:
            template_values = 'core/pc_layout.html'

        context = {
            'active': 'rc',
            'root_causes': causes,
            'template_values': template_values,
            'current_tree': current_tree
        }

        return render(request, 'causalmodel/root_causes.html', context)

    messages.error(request, 'Data is not up to date')
    return redirect('core:nutritionist')


@login_required
@not_bns
def add_root_cause(request):

    profile = Profile.objects.get(user=request.user)

    if profile.user_type == 'Nutritionist':
        layout = 'core/nutritionist-layout.html'
    else:
        layout = 'core/pc_layout.html'

    context = {
        'metrics': Metric.get_alarming(),
        'layout': layout,
        'root_causes': RootCause.objects.filter(date__year=year_now)
    }

    return render(request, 'causalmodel/add_root_cause.html', context)


@login_required
@not_bns
def create_causal_model(request):

    root_causes = RootCause.objects.filter(date__year=year_now)

    profile = Profile.objects.get(user=request.user)

    if profile.user_type == 'Nutritionist':
        layout = 'core/nutritionist-layout.html'
    else:
        layout = 'core/pc_layout.html'

    if not root_causes:
        messages.error(request, 'Please add root causes first.')
        return redirect('causalmodel:rc_index')

    context = {
        'root_causes': root_causes,
        'layout': layout
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

    causal_model = CausalModel(uploaded_by=Profile.objects.get(user=request.user))
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

    # send notification to program coordinator
    message = '%s has submitted a causal model' % Profile.objects.get(user=request.user).get_name
    Notification.objects.create(
        message=message,
        profile_to=Profile.objects.filter(user_type__contains='Program Coordinator')[0],
        profile_from=Profile.objects.get(user=request.user)
    )

    return JsonResponse(child_dict, safe=False)


def get_blocks(request):

    id = request.POST['id']
    causal = CausalModel.objects.get(id=id)

    q1 = Child.objects.filter(block__causal_model=causal)

    # get comments
    comments = [c.to_dict() for c in CausalModelComment.objects.filter(causal_model=causal).order_by('-date')]

    child_dict = [x.to_tree_dict() for x in q1]
    data = {
        'data': child_dict,
        'comments': comments
    }
    return JsonResponse(data)


@login_required
@not_bns
def insert_comment(request):

    comment = request.POST['comment']
    id = request.POST['id']

    CausalModelComment.objects.create(
        comment=comment,
        causal_model_id=id,
        profile=Profile.objects.get(user=request.user)
    )

    return JsonResponse(CausalModelComment.objects.latest('id').to_dict())


@login_required
@is_program_coordinator
def approve_model(request):

    id = request.POST['id']

    causal_model = CausalModel.objects.get(id=id)
    causal_model.is_approved = True
    causal_model.save()

    return JsonResponse({
        'Success': 'Hello'
    })


@login_required
@not_bns
def view_summary(request, metric):

    profile = Profile.objects.get(user=request.user)

    if profile.user_type == 'Nutritionist':
        layout = 'core/nutritionist-layout.html'
    else:
        layout = 'core/pc_layout.html'

    context = {
        'template_values': layout,

        'metric': Metric.objects.get(id=metric)
    }

    return render(request, 'causalmodel/view_summary.html', context)



