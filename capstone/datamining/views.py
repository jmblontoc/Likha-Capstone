
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from friends.datamining import correlations
from datainput.models import NutritionalStatus, Barangay, Sex, ChildCare
from friends.datapreprocessing import checkers
from django.shortcuts import render, redirect


# Create your views here.

@login_required
def index(request):

    if checkers.is_updated():

        nutritional_statuses = NutritionalStatus.objects.all()

        context = {
            'statuses': nutritional_statuses,
        }

        sex = Sex.objects.get(name='Female')

        # test
        print(correlations.get_weight_values_per_month(nutritional_statuses[1], sex))
        print(correlations.get_unemployment_rate())
        print(correlations.get_informal_settlers())

        return render(request, 'datamining/index.html', context)

    messages.error(request, 'Data is not up to date')
    return redirect('core:nutritionist')
