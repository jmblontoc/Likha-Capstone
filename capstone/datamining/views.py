
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from friends.datamining import correlations, forecast as f
from datainput.models import NutritionalStatus, Barangay, Sex, ChildCare, Tuberculosis, Malaria, Immunization, \
    MaternalCare, Schistosomiasis, Leprosy, Flariasis, STISurveillance
from friends.datapreprocessing import checkers
from django.shortcuts import render, redirect
from core.models import Profile, Notification
from friends import datapoints


# Create your views here.

@login_required
def index(request):

    if checkers.is_updated():

        nutritional_statuses = NutritionalStatus.objects.all()


        profile = Profile.objects.get(user=request.user)
        scores = request.session['scores']

        context = {
            'profile': profile,
            'active': 'ct',
            'statuses': nutritional_statuses,
            'scores': scores
        }

        return render(request, 'datamining/index.html', context)

    messages.error(request, 'Data is not up to date')
    return redirect('core:nutritionist')


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
