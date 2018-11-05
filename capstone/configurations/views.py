import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from capstone.decorators import is_program_coordinator, is_nutritionist, not_bns
from computations.weights import year_now
from configurations.forms import SuggestedInterventionForm
from configurations.models import CorrelationConf, NotifyBNS
from core.models import Profile
from datapreprocessing.models import Metric
from friends.datamining.clean_correlations import put_marks, get_micronutrient_revised, get_maternal_revised, \
    get_socioeconomic_revised, get_child_care_revised, trim_correlations


@login_required
@is_program_coordinator
def index(request):

    return HttpResponse('hello')


@login_required
@is_program_coordinator
def set_correlations(request):

    if request.method == 'GET':

        request.session['micronutrient'] = trim_correlations(get_micronutrient_revised())
        request.session['maternal'] = trim_correlations(get_maternal_revised())
        request.session['socioeconomic'] = trim_correlations(get_socioeconomic_revised())
        request.session['child_care'] = trim_correlations(get_child_care_revised())

        micro = put_marks(request.session['micronutrient'])
        maternal = put_marks(request.session['maternal'])
        socio = put_marks(request.session['socioeconomic'])
        child_care = put_marks(request.session['child_care'])

        context = {
            'micro': micro,
            'maternal': maternal,
            'child_care': child_care,
            'socio': socio
        }

        return render(request, 'configurations/set_correlations.html', context)

    if request.method == 'POST':

        approved = request.POST.getlist('approved')
        report = request.POST['report']

        if report == 'micro':
            CorrelationConf.objects.create(
                script=json.dumps(approved),
                report='micro'
            )

        if report == 'maternal':
            CorrelationConf.objects.create(
                script=json.dumps(approved),
                report='maternal'
            )

        if report == 'child_care':
            CorrelationConf.objects.create(
                script=json.dumps(approved),
                report='child_care'
            )

        if report == 'socio':
            CorrelationConf.objects.create(
                script=json.dumps(approved),
                report='socio',
            )

        messages.success(request, 'Correlations configured')
        return redirect('conf:index')


@login_required
@is_nutritionist
def set_notification_time(request):

    days_before = request.POST['days-before']

    current_setting = NotifyBNS.objects.first()
    current_setting.days_before = days_before
    current_setting.save()

    messages.success(request, 'All BNS will be notified %i days before the due date' % int(current_setting.days_before))
    return redirect('core:nutritionist')


@login_required
@not_bns
def set_suggested_interventions(request):

    profile = Profile.objects.get(user=request.user)

    if profile.user_type == 'Nutritionist':
        layout = 'core/nutritionist-layout.html'
    else:
        layout = 'core/pc_layout.html'

    # metrics
    metrics = Metric.objects.filter(date__year=year_now)

    context = {
        'layout': layout,
        'metrics': metrics
    }

    return render(request, 'configurations/intervention_settings.html', context)


@login_required
def ajax_get_interventions(request):

    metric = request.GET['metric']

    interventions = Metric.objects.get(id=metric).suggested_interventions

    return JsonResponse(interventions, safe=False)


@login_required
def ajax_set_interventions(request):

    interventions = request.GET['interventions']
    metric = request.GET['metric']

    m = Metric.objects.get(id=metric)
    m.suggested_interventions = interventions
    m.save()

    return JsonResponse("", safe=False)


@login_required
@not_bns
def view_interventions(request, metric_id):

    profile = Profile.objects.get(user=request.user)

    if profile.user_type == 'Nutritionist':
        layout = 'core/nutritionist-layout.html'
    else:
        layout = 'core/pc_layout.html'

    metric = Metric.objects.get(id=metric_id)

    suggested_interventions = metric.suggestedintervention_set.all()

    form = SuggestedInterventionForm(request.POST or None)

    if form.is_valid():

        intervention = form.save(commit=False)
        intervention.is_priority = False
        intervention.metric = metric
        intervention.save()

        messages.success(request, 'Intervention for %s successfully added' % metric.get_data_point)
        return redirect('conf:view_interventions', metric.id)

    context = {
        'suggested_interventions': suggested_interventions,
        'metric': metric,
        'layout': layout,
        'form': form
    }

    return render(request, 'configurations/view_interventions.html', context)

