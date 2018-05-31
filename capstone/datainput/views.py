import os
from datetime import datetime

import xlrd
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from datainput.forms import FamilyProfileForm, PatientForm, MonthlyReweighingForm
from friends.datainput import excel_uploads

from core.models import Profile
from datainput.models import OperationTimbang, NutritionalStatus, AgeGroup, OPTValues, FamilyProfile, FamilyProfileLine, \
    Patient, MonthlyReweighing


@login_required
def handle_opt_file(request):

    # error checking
    if len(request.FILES) == 0:
        messages.error(request, 'Pleae submit a file')
        return redirect('core:bns-index')

    file = request.FILES['eOPT']

    # other error checking goes here TODO

    # check if valid file type

    file_extension = os.path.splitext(file.name)

    print(file_extension[1])

    if not file_extension[1] == '.xlsx':
        messages.error(request, 'Please upload a valid excel file')
        return redirect('core:bns-index')

    # upload file
    # with open(settings.MEDIA_ROOT + file.name, 'wb+') as destination:
    #     for chunk in file.chunks():
    #         destination.write(chunk)

    path = os.path.join(settings.MEDIA_ROOT, 'eopt', file.name)
    default_storage.save(path, file)

    # handle excel file

    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_index(2)

    # error checking ulit

    if not excel_uploads.is_valid_opt(sheet):
        messages.error(request, 'There are unfilled cells in the sheet. Please fill them up')
        return redirect('core:bns-index')

    print('goes here')

    # store values in the DB

    barangay = Profile.objects.get(user=request.user).barangay
    opt = OperationTimbang(barangay=barangay)
    opt.save()

    ns_list = [
        'WN',
        'WO',
        'WU',
        'WSU',
        'HN',
        'HT',
        'HS',
        'HSS',
        'WHN',
        'WHO',
        'WHOb',
        'WHW',
        'WHSW'
    ]
    cell_columns = [1, 2, 4, 5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 20]

    age_groups = AgeGroup.objects.all()

    count = 0
    for age_group in age_groups:
        excel_uploads.upload_eopt(age_group, ns_list, cell_columns[count], opt, sheet)
        count = count + 1

    # remove file after data has been uploaded
    # os.remove(file.name)

    opt.status = 'Pending'
    opt.save()

    messages.success(request, 'eOPT successfully uploaded!')
    return redirect('core:bns-index')


@login_required
def handle_family_profile_file(request):

    # error checking
    if len(request.FILES) == 0:
        messages.error(request, 'Pleae submit a file')
        return redirect('core:bns-index')

    file = request.FILES['family_profile']

    # other error checking goes here TODO

    # check if valid file type

    file_extension = os.path.splitext(file.name)

    print(file_extension[1])

    if not file_extension[1] == '.xlsx':
        messages.error(request, 'Please upload a valid excel file')
        return redirect('core:bns-index')

    # upload file
    with open(settings.MEDIA_ROOT + file.name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


@login_required
def family_profiles(request):

    barangay = Profile.objects.get(user=request.user).barangay
    families = FamilyProfile.objects.filter(barangay=barangay, date__year=datetime.now().year)

    context = {
        'barangay': barangay,
        'families': families
    }

    return render(request, 'datainput/family_profile_index.html', context)


@login_required
def add_family_profile(request):

    barangay = Profile.objects.get(user=request.user).barangay
    form = FamilyProfileForm(request.POST or None)

    if form.is_valid():
        family = form.save(commit=False)
        check = FamilyProfile.objects.filter(date__year=datetime.now().year, barangay=barangay)

        if check.count() == 0:
            family_profile = FamilyProfile.objects.create(barangay=barangay, status='Pending')

        family_profile = check[0]

        family.family_profile = family_profile
        family.status = 'Pending'
        family.save()

        messages.success(request, 'Family profile added successfully!')
        return redirect('datainput:family_profiles')

    context = {
        'form': form
    }

    return render(request, 'datainput/add_family.html', context)


@login_required
def show_profiles(request, id):

    profiles = FamilyProfileLine.objects.filter(family_profile_id__exact=id)

    context = {
        'profiles': profiles
    }

    return render(request, 'datainput/families_list.html', context)


# ajax show profile
def show_profile_ajax(request):

    family = request.POST['family_id']
    profile = FamilyProfileLine.objects.filter(id=family)
    serialized = serializers.serialize('json', profile)

    data = {
        "profile": serialized
    }

    return JsonResponse(data)


@login_required
def monthly_reweighing_index(request):

    barangay = Profile.objects.get(user=request.user).barangay
    opt = OperationTimbang.objects.filter(barangay=barangay, date__year=datetime.now().year)
    patients = Patient.objects.filter(barangay=barangay)

    context = {
        'patients': patients,
        'has_opt': len(opt) > 0
    }

    return render(request, 'datainput/monthly_reweighing_index.html', context)


@login_required
def add_patient(request):

    barangay = Profile.objects.get(user=request.user).barangay

    form = PatientForm(request.POST or None)

    if form.is_valid():
        patient = form.save(commit=False)
        patient.barangay = barangay
        patient.save()

        messages.success(request, 'Patient added successfully!')
        return redirect('datainput:monthly_reweighing_index')

    context = {
        'form': form
    }

    return render(request, 'datainput/add_patient.html', context)


@login_required
def patient_overview(request, id):

    patient = Patient.objects.get(id=id)
    weights = MonthlyReweighing.objects.filter(patient=patient)

    context = {
        'patient': patient,
        'weights': weights,
    }

    return render(request, 'datainput/patient_overview.html', context)


@login_required
def reweigh(request, id):

    patient = Patient.objects.get(id=id)
    form = MonthlyReweighingForm(request.POST or None)

    if form.is_valid():

        updates = form.save(commit=False)
        updates.status = 'Pending'
        updates.patient = patient
        updates.save()

        messages.success(request, 'Nutritional status updated!')
        return redirect('datainput:monthly_reweighing_index')

    context = {
        'form': form
    }

    return render(request, 'datainput/monthly_reweighing_form.html', context)














