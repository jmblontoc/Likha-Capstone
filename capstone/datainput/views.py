import os
from datetime import datetime

import xlrd
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import redirect, render

from datainput.forms import FamilyProfileForm
from friends.datainput import excel_uploads

from core.models import Profile
from datainput.models import OperationTimbang, NutritionalStatus, AgeGroup, OPTValues, FamilyProfile


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
    with open(settings.MEDIA_ROOT + file.name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    # handle excel file

    workbook = xlrd.open_workbook(file.name)
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
    os.remove(file.name)

    opt.status = 'Waiting for Approval'
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
            family_profile = FamilyProfile.objects.create(barangay=barangay)
        
        family_profile = check[0]

        family.family_profile = family_profile
        family.save()

        messages.success(request, 'Family profile added successfully!')
        return redirect('datainput:family_profiles')

    context = {
        'form': form
    }

    return render(request, 'datainput/add_family.html', context)
















