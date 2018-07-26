import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from capstone.decorators import is_program_coordinator
from configurations.models import CorrelationConf
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

