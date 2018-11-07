import json
from datetime import datetime

from django.urls import reverse


from computations import weights
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from capstone.decorators import not_bns, is_program_coordinator
from core.context_processors import get_user_type, profile
from core.models import Profile, Notification
from datainput.models import Barangay
from friends.causalmodel import helper
# Create your views here.
from datapreprocessing.models import Metric
from causalmodel.models import RootCause, DataMap, Block, Child, CausalModel, CausalModelComment, Memo, Son, Box, \
    SuggestedIntervention
from friends.datamining.correlations import create_session, year_now
from friends.datapreprocessing import checkers
from friends.datamining import correlations
from friends.datainput import validations


@login_required
@not_bns
def index(request, year):

    profile = Profile.objects.get(user=request.user)

    if len(validations.todo_list()) > 0:
        messages.error(request, 'Data is not yet up to date')

        if profile.user_type == 'Nutritionist':
            return redirect('core:nutritionist')
        else:
            return redirect('core:program_coordinator')

    if Metric.objects.count() != 34:
        messages.error(request, 'Please set thresholds for all metrics')
        return redirect('datapreprocessing:set_thresholds')

    if profile.user_type == 'Nutritionist':
        layout = 'core/nutritionist-layout.html'
    else:
        layout = 'core/pc_layout.html'

    models = CausalModel.objects.filter(date__year=year).order_by('-date')

    if RootCause.objects.filter(date__year=year).count() == 0:
        roots = RootCause.show_root_causes()
        has_root_cause = False
    else:
        roots = [root_cause for root_cause in RootCause.objects.filter(date__year=year)]
        has_root_cause = True

    current_tree = CausalModel.objects.filter(date__year=year)

    years = [x.year for x in CausalModel.objects.dates('date', 'year')]

    if year_now not in years:
        years.append(year_now)
    years = sorted(years, reverse=True)
    years.insert(0, "--")

    context = {
        'active': 'cm',
        'causals': models,
        'year_get': year,
        'current': current_tree,
        'layout': layout,
        'models': CausalModel.objects.filter(date__year=year),
        'roots': roots,
        'years': years,
        'has_root_cause': has_root_cause,
        'manual_causes': serializers.serialize('json', RootCause.show_manual_root_causes())

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

    year = year_now

    if validations.todo_list().__len__() == 0:

        if year == year_now:
            causes = RootCause.show_root_causes()
        else:
            causes = RootCause.objects.filter(date__year=year)
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
        'active': 'arc',
        'metrics': Metric.objects.all(),
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

    q1 = Son.objects.filter(box__causal_model__date__year=causal.date.year)

    # get comments
    comments = [c.to_dict() for c in CausalModelComment.objects.filter(causal_model=causal).order_by('-date')]

    child_dict = [x.to_dict for x in q1]

    # put weights
    for x in child_dict:
        if 'Undernutrition' in x['name']:
            # put weights
            pass

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

    if request.method == 'GET':

        if profile.user_type == 'Nutritionist':
            layout = 'core/nutritionist-layout.html'
        else:
            layout = 'core/pc_layout.html'

        context = {
            'template_values': layout,
            'active': 'cm',
            'profile': profile,
            'metric': Metric.objects.get(id=metric),
            'barangays': json.dumps([b.name for b in Barangay.objects.all()])
        }

        return render(request, 'causalmodel/view_summary_revised.html', context)

    if request.method == 'POST':

        m = request.POST['metric']
        comments = request.POST['comments']
        subject = request.POST['subject']

        recipients = request.POST['recipients']

        interventions = request.POST.getlist('interventions')
        for_interventions = "The following interventions are suggested to address the concern for such metric: "

        for index, intervention in enumerate(interventions):
            for_interventions += '(%i) %s \n' % (index + 1, intervention)


        created = Memo.objects.create(
            metric=Metric.objects.get(id=m),
            uploaded_by=profile,
            suggested_interventions=for_interventions,
            comments=comments,
            subject=subject
        )

        # get barangays from post
        barangay_strs = recipients.split(",")

        for item in barangay_strs:

            barangay = Barangay.objects.get(name=item)
            created.barangays_addressed_to.add(barangay)

            # notify
            for profile in Profile.objects.filter(barangay=barangay):
                Notification.objects.create(
                    profile_to=profile,
                    profile_from=Profile.objects.get(user=request.user),
                    message="Memo has been released by the program coordinator (%s)" % Profile.objects.get(user=request.user).get_name
                )

        return redirect('core:memo_detail', id=created.id)


def ajax_get_metric(request):

    id = request.POST['id']
    metric = Metric.objects.get(id=id)
    trend = eval(metric.get_value_until_present)

    values = [v for k, v in trend.items()]
    start = sorted(trend.keys())[0]

    return JsonResponse({
        'data': metric.to_high_charts_d(),
        'field': metric.get_data_point,
        'trend': values,
        'start': start
    })


def dummy(request):

    context = {

    }

    return render(request, 'causalmodel/dummy.html', context)


def get_boxes(request):

    return JsonResponse({
        "data": [x.to_dict for x in Son.objects.all()]
    })


def produce_causal_model(request):

    causal_model = CausalModel(uploaded_by=Profile.objects.get(user=request.user), is_approved=True)
    causal_model.save()

    for root in RootCause.show_root_causes():
        x = RootCause.objects.create(
            name=root.name
        )

        for d in root.datamap_set.all():
            DataMap.objects.create(
                root_cause=x,
                metric=d.metric,
                value=d.to_metric.get_total_value,
                threshold=d.threshold
            )

    current_causes = RootCause.show_root_causes()

    boxes = Box.objects.filter(causal_model__date__year=2017)

    for cause in current_causes:
        for box in boxes:
            if cause == box.root_cause:
                x = Box.objects.create(
                    root_cause=cause,
                    causal_model=causal_model
                )

    no_maps = [x for x in boxes if x.root_cause.datamap_set.count() == 0]
    for x in no_maps:
        Box.objects.create(
            root_cause=x.root_cause,
            causal_model=causal_model
        )

    new_boxes = Box.objects.filter(causal_model__date__year=year_now)

    sons = Son.objects.filter(box__causal_model__date__year=year_now - 1)

    for i, bx in enumerate(new_boxes):
        for j, s in enumerate(sons):
            if bx.root_cause.name == s.box.root_cause.name:
                for k, b1 in enumerate(new_boxes):
                    if b1.root_cause.name == s.father.root_cause.name:
                        Son.objects.create(
                            box=bx,
                            father=b1
                        )
                        break

    # notify program coordinator
    Notification.objects.create(
        profile_to=Profile.objects.filter(user_type__contains='Program Coordinator')[0],
        profile_from=Profile.objects.get(user=request.user),
        message='Causal model has been created'
    )

    messages.success(request, 'Causal model successfully created')
    return redirect(reverse('causalmodel:index', kwargs={'year': year_now}) + '#tree-holder')


def get_blocks_2(request):

    year = request.POST['year']

    causal = CausalModel.objects.get(date__year=year)

    q1 = Son.objects.filter(box__causal_model__date__year=causal.date.year)

    # get comments
    comments = [c.to_dict() for c in CausalModelComment.objects.filter(causal_model=causal).order_by('-date')]

    child_dict = [x.to_dict for x in q1]

    # put weights
    for x in child_dict:
        if 'Undernutrition' in x['name']:
            # put weights
            first = weights.totals_per_category()[0]
            second = weights.totals_per_category()[1]
            third = weights.totals_per_category()[2]

            x['quantifiable_data'] = [
                'Underweight and Severely Underweight - %i' % first,
                'Stunted and Severely Stunted - %i' % second,
                'Wasted and Severely Wasted - %i' % third,
            ]

    data = {
        'data': child_dict,
        'comments': comments
    }
    return JsonResponse(data)


@login_required
@not_bns
def causal_model_report(request, year):

    causal_model = CausalModel.objects.get(date__year=year)

    context = {
        'causal_model': causal_model,
        'year': year
    }

    return render(request, 'causalmodel/causal_model_report.html', context)


@login_required
@not_bns
def delete_root_cause(request, id):

    RootCause.objects.get(id=id).delete()
    messages.success(request, 'Root cause successfully deleted')

    return redirect("/causal-models/root_cause/add")


@login_required
def append_to_causal_model(request):

    append_to = request.POST['to']
    append_item = request.POST['item']

    main_box = Box.objects.create(
        root_cause=RootCause.objects.get(id=append_item),
        causal_model=CausalModel.objects.filter(date__year=year_now)[0]
    )

    Son.objects.create(
        box=main_box,
        father=Box.objects.filter(root_cause__name__contains=append_to, causal_model__date__year=year_now).first()
    )

    return JsonResponse([], safe=False)


@login_required
def add_intervention_from_modal(request):

    metric_id = request.POST['id']
    name = request.POST['name']
    reason = request.POST['reason']

    intervention = SuggestedIntervention.objects.create(
        name=name,
        metric_id=metric_id,
        reason=reason
    )

    return JsonResponse(intervention.to_data(), safe=False)


@login_required
@not_bns
def referencing_memo(request, date, intervention_id):

    intervention = SuggestedIntervention.objects.get(id=intervention_id)

    legit_date = datetime.strptime(date, '%B %d, %Y')

    memo = Memo.objects.filter(suggested_interventions__contains=intervention.name, date__date=legit_date).first()

    return redirect('core:memo_detail', memo.id)