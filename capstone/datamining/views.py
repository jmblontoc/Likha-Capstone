
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from friends.datamining import correlations
from datainput.models import NutritionalStatus, Barangay, Sex, ChildCare
from friends.datapreprocessing import checkers
from django.shortcuts import render, redirect
from friends import datapoints


# Create your views here.

@login_required
def index(request):

    if checkers.is_updated():

        nutritional_statuses = NutritionalStatus.objects.all()

        scores = []

        # # # # # # # # # # # # #
        # MALE
        sex = Sex.objects.get(name='Female')

        for status in nutritional_statuses:
            for data in datapoints.get_child_care_fields():
                phrase = str(data).split(".")
                field = phrase[2]

                weights = correlations.get_weight_values_per_month(status, sex)
                data_point = correlations.get_fhsis(ChildCare, field, sex)
                score = correlations.get_correlation_score(
                    correlations.make_variables(weights, data_point)
                )

                scores.append(
                    {
                        'category': status.name + " - Female",
                        'source': 'Child Care',
                        'field': data.verbose_name,
                        'score': score
                    }
                )

        context = {
            'statuses': nutritional_statuses,
            'scores': scores
        }

        return render(request, 'datamining/index.html', context)

    messages.error(request, 'Data is not up to date')
    return redirect('core:nutritionist')
