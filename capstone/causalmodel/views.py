from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from datapreprocessing.models import Metric


@login_required
def index(request):

    context = {

    }

    return render(request, 'causalmodel/index.html', context)


@login_required
def root_causes(request):

    context = {

    }

    return render(request, 'causalmodel/root_causes.html', context)


@login_required
def add_root_cause(request):

    context = {

    }

    return render(request, 'causalmodel/add_root_cause.html', context)
