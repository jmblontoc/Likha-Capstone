import os
import xlrd
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import redirect

from core.models import Profile
from datainput.models import OperationTimbang


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




