import os
import xlrd
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import redirect
from friends.datainput import excel_uploads

from core.models import Profile
from datainput.models import OperationTimbang, NutritionalStatus, AgeGroup, OPTValues


def handle_opt_file(request):

    # error checking
    if len(request.FILES) == 0:
        messages.error(request, 'Pleae submit a file')
        return redirect('core:bns-index')

    # other error checking goes here TODO

    # upload file

    file = request.FILES['eOPT']
    with open(settings.MEDIA_ROOT + file.name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    # handle excel file

    workbook = xlrd.open_workbook(file.name)
    sheet = workbook.sheet_by_index(2)

    # store values in the DB

    barangay = Profile.objects.get(user=request.user).barangay
    opt = OperationTimbang(barangay=barangay)
    opt.save()

    print(excel_uploads.is_valid_opt(sheet))

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

    # # 0 - 5 months boys
    #
    # age_group = AgeGroup.objects.get(code='05', sex='Male')
    # excel_uploads.upload_eopt(age_group, ns_list, 1, opt, sheet)
    #
    # # 0 - 5 months girls
    #
    # age_group = AgeGroup.objects.get(code='05', sex='Female')
    # excel_uploads.upload_eopt(age_group, ns_list, 2, opt, sheet)
    #
    # # 6 - 11 months boys
    #
    # age_group = AgeGroup.objects.get(code='611', sex='Male')
    # excel_uploads.upload_eopt(age_group, ns_list, 4, opt, sheet)
    #
    # # 6 - 11 months girls
    #
    # age_group = AgeGroup.objects.get(code='611', sex='Female')
    # excel_uploads.upload_eopt(age_group, ns_list, 5, opt, sheet)
    #
    # # 12 - 23 months boys
    #
    # age_group = AgeGroup.objects.get(code='1223', sex='Male')
    # excel_uploads.upload_eopt(age_group, ns_list, 7, opt, sheet)
    #
    # # 12 - 23 months girls
    #
    # age_group = AgeGroup.objects.get(code='1223', sex='Female')
    # excel_uploads.upload_eopt(age_group, ns_list, 8, opt, sheet)
    #
    # # 24 - 35 months boys
    #
    # age_group = AgeGroup.objects.get(code='2435', sex='Male')
    # excel_uploads.upload_eopt(age_group, ns_list, 10, opt, sheet)
    #
    # # 24 - 35 months girls
    #
    # age_group = AgeGroup.objects.get(code='2435', sex='Female')
    # excel_uploads.upload_eopt(age_group, ns_list, 11, opt, sheet)
    #
    # # 36 - 47 months boys
    #
    # age_group = AgeGroup.objects.get(code='3647', sex='Male')
    # excel_uploads.upload_eopt(age_group, ns_list, 13, opt, sheet)
    #
    # # 36 - 47 months girls
    #
    # age_group = AgeGroup.objects.get(code='3647', sex='Female')
    # excel_uploads.upload_eopt(age_group, ns_list, 14, opt, sheet)
    #
    # # 48 - 59 months boys
    #
    # age_group = AgeGroup.objects.get(code='4859', sex='Male')
    # excel_uploads.upload_eopt(age_group, ns_list, 16, opt, sheet)
    #
    # # 48 - 59 months girls
    #
    # age_group = AgeGroup.objects.get(code='4859', sex='Female')
    # excel_uploads.upload_eopt(age_group, ns_list, 17, opt, sheet)
    #
    # # 60 - 71 months boys
    #
    # age_group = AgeGroup.objects.get(code='6071', sex='Male')
    # excel_uploads.upload_eopt(age_group, ns_list, 19, opt, sheet)
    #
    # # 60 - 71 months girls
    #
    # age_group = AgeGroup.objects.get(code='6071', sex='Female')
    # excel_uploads.upload_eopt(age_group, ns_list, 20, opt, sheet)
    #
    # # remove file after data has been uploaded
    # os.remove(file.name)
    #
    # return HttpResponse("Data uploaded!")
















