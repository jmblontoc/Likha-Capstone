import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from capstone.decorators import is_bns, is_nutritionist, is_program_coordinator, not_bns
from friends.datainput import validations
from friends import datapoints
from django.http import HttpResponse, JsonResponse
from friends.datamining import correlations, forecast as f, clean_correlations
from datainput.models import NutritionalStatus, Barangay, Sex, ChildCare, Tuberculosis, Malaria, Immunization, \
    MaternalCare, Schistosomiasis, Leprosy, Flariasis, STISurveillance
from friends.datapreprocessing import checkers
from django.shortcuts import render, redirect
from core.models import Profile, Notification
from friends import datapoints


# Create your views here.

@login_required
@not_bns
def index(request):

    # if validations.todo_list().__len__() == 0:

    nutritional_statuses = NutritionalStatus.objects.all()

    profile = Profile.objects.get(user=request.user)
    clean_correlations.create_correlation_session(request)

    micro = request.session['micronutrient']
    maternal = request.session['maternal']
    child_care = request.session['child_care']
    socio = request.session['socioeconomic']

    if profile.user_type == 'Nutritionist':
        template_values = 'core/nutritionist-layout.html'
    else:
        template_values = 'core/pc_layout.html'

    context = {
        'profile': profile,
        'template_values': template_values,
        'active': 'ct',
        'statuses': nutritional_statuses,
        'micro': micro,
        'maternal': maternal,
        'child_care': child_care,
        'socio': socio

    }

    return render(request, 'datamining/revised_index.html', context)

    # messages.error(request, 'Data is not up to date')
    # return redirect('core:nutritionist')


@login_required
def get_variables(request):

    category = request.POST['category']
    source = request.POST['source']
    field = request.POST['field']

    if source == 'Maternal Care':

        for m in request.session['maternal']:
            if m['category'] == category and m['source'] == source and m['field'] == field:
                data = {
                    'variables': m['variables']
                }
                return JsonResponse(data, safe=False)


    elif source == 'Child Care' or source == 'Malaria' or source == 'Immunization' or source == 'Tuberculosis':

        for m in request.session['child_care'] + request.session['micronutrient']:
            if m['category'] == category and m['source'] == source and m['field'] == field:
                return JsonResponse({
                    'variables': m['variables']
                })

    elif source == 'Family Profile':

        for m in request.session['socioeconomic']:
            if m['category'] == category and m['source'] == source and m['field'] == field:
                return JsonResponse({
                    'variables': m['variables']
                })


@login_required
def get_variables_v2(request):
    source = request.POST['source']
    field = request.POST['field']

    if source == 'Maternal Care':
        data = []
        for m in request.session['maternal']:
            if m['source'] == source and m['field'] == field:
                data = [variables for variables in m['data']]

        return JsonResponse({'variables': data, 'source': source})

    elif source == 'Child Care' or source == 'Malaria' or source == 'Immunization' or source == 'Tuberculosis':
        data = []
        for m in request.session['child_care'] + request.session['micronutrient']:
            if m['source'] == source and m['field'] == field:
                data = [variables for variables in m['data']]

        return JsonResponse({'variables': data, 'source': source})

    elif source == 'Family Profile':
        data = []
        for m in request.session['socioeconomic']:
            if m['source'] == source and m['field'] == field:
                data = [variables for variables in m['data']]

        return JsonResponse({'variables': data, 'source': source})





@login_required
def get_positive(request):

    correlations = request.session['scores']
    profile = Profile.objects.get(user=request.user)

    scores = [x for x in correlations if x['score'] > 0]

    context = {
        'profile': profile,
        'active': 'ct',
        'scores': scores
    }

    return render(request, 'datamining/index.html', context)


# predictive modeling page
@login_required
def forecast(request, id):

    correlation = request.session['scores']

    cr_line = correlation[id]
    score = cr_line['score']
    variables = cr_line['variables']
    equation = f.get_equation_string(score, variables)

    context = {
        'cr': cr_line,
        'equation': equation,
        'variables': variables,
        'line': f.get_line(score, variables),
        'equation_variables': f.get_variables(score, variables)
    }

    return render(request, 'datamining/forecast.html', context)
