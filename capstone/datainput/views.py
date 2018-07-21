
import os
from datetime import datetime, date
import xlrd
from django.views import View
from xlutils.copy import copy
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models import Count
from decimal import *

from capstone.decorators import is_bns, is_nutritionist
from core.forms import RejectForm
from datainput.forms import FamilyProfileForm, PatientForm, MonthlyReweighingForm, HealthCareWasteManagementForm, \
    InformalSettlersForm, UnemploymentRateForm
from friends.datainput import excel_uploads, validations, misc
from core.models import Profile, Notification
from datainput.models import OperationTimbang, NutritionalStatus, AgeGroup, OPTValues, FamilyProfile, FamilyProfileLine, \
    Patient, MonthlyReweighing, HealthCareWasteManagement, InformalSettlers, UnemploymentRate, Barangay, FHSIS, \
    MaternalCare, STISurveillance, Immunization, Sex, Malaria, Tuberculosis, Schistosomiasis, Flariasis, Leprosy, \
    ChildCare


@login_required
@is_bns
def handle_opt_file(request):

    # error checking
    if len(request.FILES) == 0:
        messages.error(request, 'Please submit a file')
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

    barangay = Profile.objects.get(user=request.user).barangay
    opt = OperationTimbang(barangay=barangay)
    opt.uploaded_by = Profile.objects.get(user=request.user)
    opt.save()

    path = os.path.join(settings.MEDIA_ROOT, 'eopt', file.name)
    temp_path = os.path.join(settings.MEDIA_ROOT, 'eopt')
    default_storage.save(path, file)

    renamed = os.path.join(temp_path, str(opt.id) + ".xlsx")
    os.rename(path, renamed)

    # handle excel file

    workbook = xlrd.open_workbook(renamed)
    sheet = workbook.sheet_by_index(2)

    # error checking ulit

    if not excel_uploads.is_valid_opt(sheet):
        opt.delete()
        os.remove(renamed)
        messages.error(request, 'There are unfilled cells in the sheet. Please fill them up')
        return redirect('core:bns-index')

    print('goes here')

    # store values in the DB

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
def show_opt_list(request):

    barangay = Profile.objects.get(user=request.user).barangay
    opt_records = OperationTimbang.objects.filter(barangay=barangay)

    profile = Profile.objects.get(user=request.user)

    print(request.META.get('HTTP_REFERER'))

    context = {
        'active':'ot',
        'profile': profile,
        'opt_records': opt_records
    }

    return render(request, 'datainput/show_opt_list.html', context)


@login_required
def view_opt_file(request, id):

    opt = OperationTimbang.objects.get(id=id)
    file_name = str(opt.id) + '.xlsx'
    file = os.path.join(settings.MEDIA_ROOT, 'eopt', file_name)

    os.startfile(file)
    return redirect('datainput:show_opt_list')


@login_required
def show_fhsis_list(request):

    barangay = Profile.objects.get(user=request.user).barangay
    fhsis_records = FHSIS.objects.filter(barangay=barangay)

    profile = Profile.objects.get(user=request.user)

    context = {
        'active': 'fh',
        'profile': profile,
        'fhsis_records': fhsis_records
    }

    return render(request, 'datainput/show_fhsis_list.html', context)


@login_required
def view_fhsis_file(request, id):

    fhsis = FHSIS.objects.get(id=id)
    file_name = str(fhsis.id) + '.xlsx'
    file = os.path.join(settings.MEDIA_ROOT, 'fhsis', file_name)

    # os.startfile(file)

    profile = Profile.objects.get(user=request.user)

    if profile.user_type == 'Nutritionist':
        return redirect('datainput:show_fhsis', fhsis.barangay.id)

    return redirect('datainput:show_fhsis_list')


@login_required
def handle_family_profile_file(request):

    # error checking
    if len(request.FILES) == 0:
        messages.error(request, 'Please submit a file')
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
    families = FamilyProfile.objects.filter(barangay=barangay)
    profile = Profile.objects.get(user=request.user)

    print(families)

    active = 'fp'

    context = {
        'active': active,
        'profile': profile,
        'barangay': barangay,
        'families': families
    }

    return render(request, 'datainput/family_profile_index.html', context)


@login_required
def monthly_reweighing_list(request):

    barangay = Profile.objects.get(user=request.user).barangay
    families = Patient.objects.values('date_created').annotate(dcount=Count('date_created'))

    profile = Profile.objects.get(user=request.user)

    print(families)

    active = 'mr'

    context = {
        'active': active,
        'profile': profile,
        'barangay': barangay,
        'families': families
    }

    return render(request, 'datainput/monthly_reweighing_list.html', context)


@login_required
@is_bns
def add_family_profile(request):

    profile = Profile.objects.get(user=request.user)
    barangay = profile.barangay

    if barangay.has_family_profile:
        messages.error(request, 'Family profile for this year has already been uploaded')
        return redirect('datainput:family_profiles')

    FamilyProfile.objects.create(uploaded_by=profile, barangay=barangay)
    messages.success(request, 'Family profile record created. You may add families now')
    return redirect('datainput:family_profiles')


@login_required
def view_family_uploaded(request):

    year = datetime.now().year
    profile = Profile.objects.get(user=request.user)
    family_profile = FamilyProfile.objects.get(barangay=profile.barangay, date__year=year)

    return redirect('datainput:show_profiles', family_profile.id)


@login_required
def show_profiles(request, id):

    profiles = FamilyProfileLine.objects.filter(family_profile_id__exact=id)
    families = FamilyProfile.objects.get(id=id)
    barangay = Barangay.objects.get(name=families.barangay.name)
    profile = Profile.objects.get(user=request.user)

    form = FamilyProfileForm(request.POST or None)

    if form.is_valid():

        f = form.save(commit=False)
        f.family_profile = families
        f.save()
        messages.success(request, 'Family added')
        return redirect('datainput:show_profiles', families.id)

    if profile.user_type == 'Barangay Nutrition Scholar':
        template_values = 'core/bns-layout.html'
    else:
        template_values = 'core/nutritionist-layout.html'
        
    context = {
        'template_values': template_values,
        'profile': profile,
        'barangay': barangay.id,
        'profiles': profiles,
        'id': id,
        'form': form
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
    profile = Profile.objects.get(user=request.user)

    context = {
        'active': 'mr',
        'profile': profile,
        'patients': patients,
        'has_opt': len(opt) > 0,
        'barangay': barangay
    }

    return render(request, 'datainput/monthly_reweighing_index.html', context)


@login_required
def latest_monthly_reweighing_index(request):

    barangay = Profile.objects.get(user=request.user).barangay
    opt = OperationTimbang.objects.filter(barangay=barangay, date__year=datetime.now().year)
    profile = Profile.objects.get(user=request.user)

    patients = Patient.objects.filter(barangay=barangay)
    patients_now = patients.filter(date_created__year=datetime.now().year)
    request.session['active'] = 'mw'
    print(request.session['active'])
    print(patients_now)

    if patients_now.count == 0:
        patients_now = patients

    context = {
        'active': 'mw',
        'profile': profile,
        'patients': set(patients_now),
        'has_opt': len(opt) > 0,
        'barangay': barangay
    }

    return render(request, 'datainput/monthly_reweighing_index.html', context)


@login_required
@is_bns
def add_patient(request):

    barangay = Profile.objects.get(user=request.user).barangay

    form = PatientForm(request.POST or None)

    if form.is_valid():
        patient = form.save(commit=False)
        patient.barangay = barangay
        patient.save()

        messages.success(request, 'Patient added successfully!')
        return redirect('datainput:monthly_reweighing_index')

    profile = Profile.objects.get(user=request.user)

    context = {
        'active': 'mw',
        'profile': profile,
        'form': form
    }

    return render(request, 'datainput/add_patient.html', context)


@login_required
def patient_overview(request, id):

    patient = Patient.objects.get(id=id)
    weights = MonthlyReweighing.objects.filter(patient=patient)
    barangay = Barangay.objects.get(name=patient.barangay.name)
    profile = Profile.objects.get(user=request.user)

    if profile.user_type == 'Barangay Nutrition Scholar':
        template_values = 'core/bns-layout.html'
    else:
        template_values = 'core/nutritionist-layout.html'

    print(request.META.get('HTTP_REFERER'))

    context = {
        'patient': patient,
        'template_values': template_values,
        'active': request.session['active'],
        'profile': profile,
        'barangay': barangay.id,
        'weights': weights,
        'is_bns': profile.user_type == 'Barangay Nutrition Scholar'
    }

    return render(request, 'datainput/patient_overview.html', context)


@login_required
@is_bns
def reweigh(request, id):

    patient = Patient.objects.get(id=id)

    if validations.is_updated(patient):
        messages.error(request, 'Nutritional status is already updated')
        return redirect('datainput:patient_overview', patient.id)

    form = MonthlyReweighingForm(request.POST or None)

    if form.is_valid():

        updates = form.save(commit=False)
        updates.status = 'Pending'
        updates.patient = patient
        updates.uploaded_by = Profile.objects.get(user=request.user)
        updates.save()

        messages.success(request, 'Nutritional status updated!')
        return redirect('datainput:monthly_reweighing_index')

    profile = Profile.objects.get(user=request.user)

    context = {
        'patient': patient,
        'profile': profile,
        'form': form
    }

    return render(request, 'datainput/monthly_reweighing_form.html', context)


@login_required
@is_nutritionist
def nutritionist_upload(request):

    has_health_care = validations.has_health_care()
    has_informal = validations.has_informal_settlers()
    has_ur = validations.has_unemployment_rate()

    profile = Profile.objects.get(user=request.user)

    context = {
        'profile': profile,
        'has_health_care': has_health_care,
        'active': 'du',
        'has_informal': has_informal,
        'has_ur': has_ur
    }

    return render(request, 'datainput/nutritionist_upload.html', context)


@login_required
@is_nutritionist
def health_care_waste_management_index(request):

    hcwm = HealthCareWasteManagement.objects.all()

    profile = Profile.objects.get(user=request.user)

    context = {
        'profile': profile,
        'active': 'du',
        'hcwm': hcwm,
    }

    return render(request, 'datainput/hcwm_index.html', context)


@login_required
@is_nutritionist
def add_hcwm(request):

    if validations.has_health_care():

        messages.error(request, 'Record for this year has already been uploaded')
        return redirect('datainput:health_care_index')

    form = HealthCareWasteManagementForm(request.POST or None)

    profile = Profile.objects.get(user=request.user)

    context = {
        'profile': profile,
        'active': 'du',
        'form': form
    }

    if form.is_valid():

        record = form.save(commit=False)
        record.save()

        messages.success(request, 'Record successfully uploaded')
        return redirect('datainput:health_care_index')

    return render(request, 'datainput/add_hcwm.html', context)


# ajax for health care waste management
def get_health_care_waste_record(request):

    id = request.POST['id']

    record = [HealthCareWasteManagement.objects.get(id=id)]

    serialized = serializers.serialize('json', record)

    data = {
        "record": serialized
    }

    return JsonResponse(data)


# informal settlers
@login_required
def informal_settlers_index(request):

    records = InformalSettlers.objects.all()
    form = InformalSettlersForm(request.POST or None)
    has_record = validations.has_informal_settlers()

    if form.is_valid():

        record = form.save(commit=False)
        record.save()

        messages.success(request, 'Data successfully uploaded')
        return redirect('datainput:informal_settlers_index')

    profile = Profile.objects.get(user=request.user)

    context = {
        'profile': profile,
        'active': 'du',
        'records': records,
        'form': form,
        'has_record': has_record
    }

    return render(request, 'datainput/informal_settlers.html', context)


# unemployment rate
@login_required
def unemployment_rate_index(request):

    records = UnemploymentRate.objects.all()
    form = UnemploymentRateForm(request.POST or None)

    if form.is_valid():

        record = form.save(commit=False)
        record.save()

        messages.success(request, 'Data successfully uploaded')
        return redirect('datainput:unemployment_rate_index')

    profile = Profile.objects.get(user=request.user)

    context = {
        'profile': profile,
        'active': 'du',
        'form': form,
        'records': records,
        'has_record': validations.has_unemployment_rate()
    }

    return render(request, 'datainput/unemployment_rate.html', context)


# data status index
@login_required
@is_nutritionist
def data_status_index(request):

    barangays = Barangay.objects.all()

    profile = Profile.objects.get(user=request.user)

    context = {
        'profile': profile,
        'active': 'ds',
        'barangays': barangays
    }

    return render(request, 'datainput/data_status_index.html', context)


@login_required
def show_opt(request, id):

    barangay = Barangay.objects.get(id=id)

    opt = OperationTimbang.objects.filter(barangay=barangay)

    profile = Profile.objects.get(user=request.user)

    context = {
        'profile': profile,
        'active': 'ds',
        'opt': opt,
        'barangay': barangay,
    }


    return render(request, 'datainput/show_opt.html', context)


@login_required
def show_fhsis(request, id):

    barangay = Barangay.objects.get(id=id)
    fhsis = FHSIS.objects.filter(barangay=barangay)

    profile = Profile.objects.get(user=request.user)

    form = RejectForm(request.POST or None)

    user_from = Profile.objects.get(user=request.user)
    user_to = fhsis[0].uploaded_by

    if form.is_valid():
        n = form.save(commit=False)
        n.profile_to = user_to
        n.profile_from = user_from
        n.save()

        fhsis.delete()

        messages.success(request, 'FHSIS record rejected.')
        return redirect('datainput:data_status_index')

    context = {
        'profile': profile,
        'active': 'ds',
        'fhsis': fhsis,
        'barangay': barangay,
        'form': form
    }

    return render(request, 'datainput/show_fhsis.html', context)


# This view lets the nutritionists view the opt and decide whether to approve or not
@login_required
def evaluate_opt(request, id, opt_id):

    opt_values = OPTValues.objects.filter(opt_id=opt_id)
    age_groups = AgeGroup.objects.all()
    nutritional_statuses = NutritionalStatus.objects.all()

    context = {
        'opt_values': opt_values,
        'age_groups': age_groups,
        'nutritional_statuses': nutritional_statuses
    }

    return render(request, 'datainput/opt_evaluation.html', context)


@login_required
def accept_opt(request, id, opt_id):

    opt = OperationTimbang.objects.get(id=opt_id)
    opt.status = 'Approved'
    opt.save()

    msg = 'Your OPT upload has been approved'
    user_from = Profile.objects.get(user=request.user)
    user_to = opt.uploaded_by

    Notification.objects.create(
        message=msg,
        profile_to=user_to,
        profile_from=user_from
    )

    messages.success(request, 'OPT validated successfully')
    return redirect('datainput:data_status_index')


@login_required
def reject_opt(request, id, opt_id):

    opt = OperationTimbang.objects.get(id=opt_id)

    msg = 'Your OPT upload has been rejected. Please re-upload the eOPT'
    user_from = Profile.objects.get(user=request.user)
    user_to = opt.uploaded_by

    Notification.objects.create(
        message=msg,
        profile_to=user_to,
        profile_from=user_from
    )

    opt.delete()

    messages.success(request, 'OPT rejected')
    return redirect('datainput:data_status_index')


@login_required
def accept_fhsis(request, id, fhsis_id):

    fhsis = FHSIS.objects.get(id=fhsis_id)
    fhsis.status = 'Approved'
    fhsis.save()

    msg = 'Your OPT upload has been approved'
    user_from = Profile.objects.get(user=request.user)
    user_to = fhsis.uploaded_by

    Notification.objects.create(
        message=msg,
        profile_to=user_to,
        profile_from=user_from
    )

    messages.success(request, 'FHSIS validated successfully')
    return redirect('datainput:data_status_index')


@login_required
def reject_fhsis(request, id, fhsis_id):

    fhsis = FHSIS.objects.get(id=fhsis_id)

    form = RejectForm(request.POST or None)

    user_from = Profile.objects.get(user=request.user)
    user_to = fhsis.uploaded_by

    if form.is_valid():
        n = form.save(commit=False)
        n.profile_to = user_to
        n.profile_from = user_from
        n.save()

        fhsis.delete()

        messages.success(request, 'FHSIS record rejected.')
        return redirect('datainput:data_status_index')

    context = {
        'form': form
    }

    return render(request, 'core/reject_form.html', context)


@login_required
def view_reweighing(request, id):

    barangay = Barangay.objects.get(id=id)
    opt = OperationTimbang.objects.filter(barangay=barangay, date__year=datetime.now().year)
    patients = Patient.objects.filter(barangay=barangay)

    profile = Profile.objects.get(user=request.user)

    context = {
        'profile': profile,
        'active': 'ds',
        'patients': patients,
        'has_opt': len(opt) > 0,
        'barangay': barangay
    }

    return render(request, 'datainput/view_reweighing.html', context)


@login_required
def accept_reweighing(request, id):

    barangay = Barangay.objects.get(id=id)
    records = MonthlyReweighing.objects.filter(patient__barangay=barangay, date__month=datetime.now().month)

    if records.count() > 0:
        for record in records:
            record.status = 'Approved'
            record.save()

        msg = 'Your Monthly Reweighing upload has been approved'
        user_from = Profile.objects.get(user=request.user)
        user_to = records[0].uploaded_by

        Notification.objects.create(
            message=msg,
            profile_to=user_to,
            profile_from=user_from
        )

        messages.success(request, 'Monthly Reweighing validated successfully')
        return redirect('datainput:data_status_index')


@login_required
def reject_reweighing(request, id):

    barangay = Barangay.objects.get(id=id)
    records = MonthlyReweighing.objects.filter(patient__barangay=barangay, date__month=datetime.now().month)

    if records.count() > 0:
        msg = 'Your Monthly Reweighing upload has been rejected. Please re-upload the reweighing records again.'
        user_from = Profile.objects.get(user=request.user)
        user_to = records[0].uploaded_by

        Notification.objects.create(
            message=msg,
            profile_to=user_to,
            profile_from=user_from
        )

        records.delete()

        messages.success(request, 'Reweighing Records rejected')
        return redirect('datainput:data_status_index')


@login_required
def show_family_profiles(request, id):

    barangay = Barangay.objects.get(id=id)
    profiles = FamilyProfile.objects.filter(barangay=barangay)
    profile = Profile.objects.get(user=request.user)

    context = {
        'profile': profile,
        'families': profiles,
        'barangay': barangay
    }

    return render(request, 'datainput/family_profiles_list.html', context)


@login_required
def accept_family_profiles(request, id):

    barangay = Barangay.objects.get(id=id)

    profile = FamilyProfile.objects.get(barangay=barangay, date__year=datetime.now().year)

    profile.status = 'Approved'
    profile.save()

    msg = 'Your Family Profile upload has been approved.'
    user_from = Profile.objects.get(user=request.user)
    user_to = profile.uploaded_by

    Notification.objects.create(
        message=msg,
        profile_to=user_to,
        profile_from=user_from
    )

    messages.success(request, 'Family profiles successfully validated')
    return redirect('datainput:data_status_index')


@login_required
def reject_family_profiles(request, id):

    barangay = Barangay.objects.get(id=id)

    profile = FamilyProfile.objects.get(barangay=barangay, date__year=datetime.now().year)

    msg = 'Your Family Profile upload has been rejected. Please re-upload the family profiles again.'
    user_from = Profile.objects.get(user=request.user)
    user_to = profile.uploaded_by

    Notification.objects.create(
        message=msg,
        profile_to=user_to,
        profile_from=user_from
    )

    profile.delete()

    messages.success(request, 'Family profiles rejected')
    return redirect('datainput:data_status_index')


@login_required
@is_bns
def handle_fhsis_file(request):

    # error checking
    if len(request.FILES) == 0:
        messages.error(request, 'Please submit a file')
        return redirect('core:bns-index')

    file = request.FILES['fhsis']

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

    path = os.path.join(settings.MEDIA_ROOT, 'fhsis', file.name)
    temp_path = os.path.join(settings.MEDIA_ROOT, 'fhsis')
    default_storage.save(path, file)

    barangay = Profile.objects.get(user=request.user).barangay
    fhsis = FHSIS(barangay=barangay, uploaded_by=Profile.objects.get(user=request.user))
    fhsis.save()
    renamed = os.path.join(temp_path, str(fhsis.id) + ".xlsx")
    os.rename(path, renamed)

    profile = Profile.objects.get(user=request.user)

    # handle excel file

    workbook = xlrd.open_workbook(renamed)
    sheet = workbook.sheet_by_index(0)

    if not excel_uploads.is_valid_fhsis(sheet):
        rows = excel_uploads.return_incomplete_fhsis(sheet)

        if len(rows) > 5:
            messages.error(request, 'FHSIS file contains many incomplete fields. Upload again')
            fhsis.delete()
            os.remove(renamed)
            return redirect('core:bns-index')

        else:
            context = {
                'rows': rows,
                'fhsis': fhsis,
                'file': renamed,
                'profile': profile,
                'active': 'uf',
            }

            for row in rows:
                if row['value'] != '':
                    try:
                        value = int(row['value'])
                    except:
                        print(row['value'])
                        messages.error(request, 'FHSIS file contains strings. Upload again')
                        fhsis.delete()
                        os.remove(renamed)
                        return redirect('core:bns-index')

            fhsis.delete()

            return render(request, 'datainput/complete_fields.html', context)


    # maternal care
    maternal_fields = misc.get_fields(MaternalCare)[1:10]

    mc = MaternalCare(fhsis=fhsis)

    counter_mc = 0
    for x in range(4, 13):
        setattr(mc, maternal_fields[counter_mc], sheet.cell_value(x, 1))
        counter_mc = counter_mc + 1

    mc.save()

    # sti surveillance
    sti_fields = misc.get_fields(STISurveillance)[2:]
    sti = STISurveillance(fhsis=fhsis)

    counter_sti = 0
    for x in range(64, 67):
        setattr(sti, sti_fields[counter_sti], sheet.cell_value(x, 1))
        counter_sti = counter_sti + 1
    sti.save()

    # immunization
    immunization_fields = misc.get_fields(Immunization)[1:11]
    immunization_male = Immunization(fhsis=fhsis, sex=Sex.objects.get(name='Male'))
    immunization_female = Immunization(fhsis=fhsis, sex=Sex.objects.get(name='Female'))

    counter_immune = 0
    for x in range(18, 21):

        # male
        setattr(immunization_male, immunization_fields[counter_immune], sheet.cell_value(x, 1))
        # female
        setattr(immunization_female, immunization_fields[counter_immune], sheet.cell_value(x, 2))

        counter_immune = counter_immune + 1

    for x in range(70, 77):

        setattr(immunization_male, immunization_fields[counter_immune], sheet.cell_value(x, 1))
        setattr(immunization_female, immunization_fields[counter_immune], sheet.cell_value(x, 2))

        counter_immune = counter_immune + 1

    immunization_female.save()
    immunization_male.save()

    # malaria
    malaria_fields = misc.get_fields(Malaria)[1:6]
    malaria_male = Malaria(fhsis=fhsis, sex=Sex.objects.get(name='Male'))
    malaria_female = Malaria(fhsis=fhsis, sex=Sex.objects.get(name='Female'))
    counter_malaria = 0

    for x in range(23, 28):
        setattr(malaria_male, malaria_fields[counter_malaria], sheet.cell_value(x, 1))
        setattr(malaria_female, malaria_fields[counter_malaria], sheet.cell_value(x, 2))
        counter_malaria = counter_malaria + 1

    malaria_male.save()
    malaria_female.save()

    # tuberculosis

    tb_fields = misc.get_fields(Tuberculosis)[1:5]
    tb_male = Tuberculosis(fhsis=fhsis, sex=Sex.objects.get(name='Male'))
    tb_female = Tuberculosis(fhsis=fhsis, sex=Sex.objects.get(name='Female'))
    counter_tb = 0

    for x in range(30, 34):
        setattr(tb_male, tb_fields[counter_tb], sheet.cell_value(x, 1))
        setattr(tb_female, tb_fields[counter_tb], sheet.cell_value(x, 2))
        counter_tb = counter_tb + 1

    tb_male.save()
    tb_female.save()

    # schistosomiasis
    schisto_fields = misc.get_fields(Schistosomiasis)[1:3]
    schisto_male = Schistosomiasis(fhsis=fhsis, sex=Sex.objects.get(name='Male'))
    schisto_female = Schistosomiasis(fhsis=fhsis, sex=Sex.objects.get(name='Female'))
    sc_counter = 0

    for x in range(36, 38):
        setattr(schisto_male, schisto_fields[sc_counter], sheet.cell_value(x, 1))
        setattr(schisto_female, schisto_fields[sc_counter], sheet.cell_value(x, 2))
        sc_counter = sc_counter + 1

    schisto_male.save()
    schisto_female.save()

    # flariasis

    flariasis_fields = misc.get_fields(Flariasis)[1:4]
    flariasis_male = Flariasis(fhsis=fhsis, sex=Sex.objects.get(name='Male'))
    flariasis_female = Flariasis(fhsis=fhsis, sex=Sex.objects.get(name='Female'))
    flariasis_counter = 0

    for x in range(40, 43):
        setattr(flariasis_male, flariasis_fields[flariasis_counter], sheet.cell_value(x, 1))
        setattr(flariasis_female, flariasis_fields[flariasis_counter], sheet.cell_value(x, 2))
        flariasis_counter = flariasis_counter + 1

    flariasis_male.save()
    flariasis_female.save()

    # leprosy

    leprosy_fields = misc.get_fields(Leprosy)[1:3]
    leprosy_male = Leprosy(fhsis=fhsis, sex=Sex.objects.get(name='Male'))
    leprosy_female = Leprosy(fhsis=fhsis, sex=Sex.objects.get(name='Female'))
    leprosy_counter = 0

    for x in range(45, 47):
        setattr(leprosy_male, leprosy_fields[leprosy_counter], sheet.cell_value(x, 1))
        setattr(leprosy_female, leprosy_fields[leprosy_counter], sheet.cell_value(x, 2))
        leprosy_counter = leprosy_counter + 1

    leprosy_male.save()
    leprosy_female.save()

    # child care
    child_care_fields = misc.get_fields(ChildCare)[1:13]
    child_care_male = ChildCare(fhsis=fhsis, sex=Sex.objects.get(name='Male'))
    child_care_female = ChildCare(fhsis=fhsis, sex=Sex.objects.get(name='Female'))
    child_care_counter = 0

    for x in range(49, 61):
        setattr(child_care_male, child_care_fields[child_care_counter], sheet.cell_value(x, 1))
        setattr(child_care_female, child_care_fields[child_care_counter], sheet.cell_value(x, 2))
        child_care_counter = child_care_counter + 1

    child_care_male.save()
    child_care_female.save()


    messages.success(request, 'FHSIS successfully uploaded')
    return redirect('core:bns-index')


    # error checking ulit


@login_required
def reports_archive(request):

    context = {

    }

    return render(request, 'datainput/archives.html', context)


@login_required
def select_report(request):

    post = request.POST['report']

    if post == 'fhsis':
        return redirect('datainput:show_fhsis_list')
    elif post == 'mr':
        return redirect('datainput:monthly_reweighing_index')
    elif post == 'opt':
        return redirect('datainput:show_opt_list')
    elif post == 'fp':
        return redirect('datainput:family_profiles')


@login_required
def complete_fields(request):

    my_dict = dict(request.POST)
    print(my_dict)
    print('asdasfwrg')
    workbook = xlrd.open_workbook(my_dict.get('path')[0])
    print(workbook)
    sheet = workbook.sheet_by_index(0)
    print(sheet)

    profile = Profile.objects.get(user=request.user)
    fhsis = FHSIS(barangay=profile.barangay, uploaded_by=profile)
    fhsis.save()
    maternal_fields = misc.get_fields(MaternalCare)[1:10]

    mc = MaternalCare(fhsis=fhsis)

    counter_mc = 0
    for x in range(4, 13):
        if sheet.cell_value(x, 1) != '':
            setattr(mc, maternal_fields[counter_mc], sheet.cell_value(x, 1) or 0)
        else:
            inlist = list(my_dict)
            inlist = inlist[2:]
            for tests in inlist:
                test = my_dict.get(tests)[0]
                test1 = tests.split("-")
                if int(test1[0]) == x:
                    setattr(mc, maternal_fields[counter_mc], Decimal(test))
        counter_mc = counter_mc + 1

    mc.save()

    # sti surveillance
    sti_fields = misc.get_fields(STISurveillance)[2:]
    sti = STISurveillance(fhsis=fhsis)

    counter_sti = 0
    for x in range(64, 67):
        if sheet.cell_value(x, 1) != '':
            setattr(sti, sti_fields[counter_sti], sheet.cell_value(x, 1) or 0)
        else:
            inlist = list(my_dict)
            inlist = inlist[2:]
            for tests in inlist:
                test = my_dict.get(tests)[0]
                test1 = tests.split("-")
                if int(test1[0]) == x:
                    setattr(sti, sti_fields[counter_sti], Decimal(test))

        counter_sti = counter_sti + 1

    sti.save()

    # immunization
    immunization_fields = misc.get_fields(Immunization)[1:11]
    immunization_male = Immunization(fhsis=fhsis, sex=Sex.objects.get(name='Male'))
    immunization_female = Immunization(fhsis=fhsis, sex=Sex.objects.get(name='Female'))

    counter_immune = 0
    for x in range(18, 21):
        if sheet.cell_value(x, 1) != '':
            setattr(immunization_male, immunization_fields[counter_immune], sheet.cell_value(x, 1) or 0)
        else:
            inlist = list(my_dict)
            inlist = inlist[2:]
            for tests in inlist:
                test = my_dict.get(tests)[0]
                test1 = tests.split("-")
                if int(test1[0]) == x:
                    setattr(immunization_male, immunization_fields[counter_immune], Decimal(test))

        if sheet.cell_value(x, 2) != '':
            setattr(immunization_female, immunization_fields[counter_immune], sheet.cell_value(x, 2) or 0)
        else:
            inlist = list(my_dict)
            inlist = inlist[2:]
            for tests in inlist:
                test = my_dict.get(tests)[0]
                test1 = tests.split("-")
                if int(test1[0]) == x:
                    setattr(immunization_female, immunization_fields[counter_immune], Decimal(test))

        counter_immune = counter_immune + 1

    for x in range(70, 77):
        if sheet.cell_value(x, 1) != '':
            setattr(immunization_male, immunization_fields[counter_immune], sheet.cell_value(x, 1) or 0)
        else:
            inlist = list(my_dict)
            inlist = inlist[2:]
            for tests in inlist:
                test = my_dict.get(tests)[0]
                test1 = tests.split("-")
                if int(test1[0]) == x:
                    setattr(immunization_male, immunization_fields[counter_immune], Decimal(test))

        if sheet.cell_value(x, 2) != '':
            setattr(immunization_female, immunization_fields[counter_immune], sheet.cell_value(x, 2) or 0)
        else:
            inlist = list(my_dict)
            inlist = inlist[2:]
            for tests in inlist:
                test = my_dict.get(tests)[0]
                test1 = tests.split("-")
                if int(test1[0]) == x:
                    setattr(immunization_female, immunization_fields[counter_immune], Decimal(test))

        counter_immune = counter_immune + 1

    immunization_female.save()
    immunization_male.save()

    # malaria
    malaria_fields = misc.get_fields(Malaria)[1:6]
    malaria_male = Malaria(fhsis=fhsis, sex=Sex.objects.get(name='Male'))
    malaria_female = Malaria(fhsis=fhsis, sex=Sex.objects.get(name='Female'))
    counter_malaria = 0

    for x in range(23, 28):
        if sheet.cell_value(x, 1) != '':
            setattr(malaria_male, malaria_fields[counter_malaria], sheet.cell_value(x, 1) or 0)
        else:
            inlist = list(my_dict)
            inlist = inlist[2:]
            for tests in inlist:
                test = my_dict.get(tests)[0]
                test1 = tests.split("-")
                if int(test1[0]) == x:
                    setattr(malaria_male, malaria_fields[counter_malaria], Decimal(test))

        if sheet.cell_value(x, 2) != '':
            setattr(malaria_female, malaria_fields[counter_malaria], sheet.cell_value(x, 2) or 0)
        else:
            inlist = list(my_dict)
            inlist = inlist[2:]
            for tests in inlist:
                test = my_dict.get(tests)[0]
                test1 = tests.split("-")
                if int(test1[0]) == x:
                    setattr(malaria_female, malaria_fields[counter_malaria], Decimal(test))
        counter_malaria = counter_malaria + 1

    malaria_male.save()
    malaria_female.save()

    # tuberculosis

    tb_fields = misc.get_fields(Tuberculosis)[1:5]
    tb_male = Tuberculosis(fhsis=fhsis, sex=Sex.objects.get(name='Male'))
    tb_female = Tuberculosis(fhsis=fhsis, sex=Sex.objects.get(name='Female'))
    counter_tb = 0

    for x in range(30, 34):
        if sheet.cell_value(x, 1) != '':
            setattr(tb_male, tb_fields[counter_tb], sheet.cell_value(x, 1) or 0)
        else:
            inlist = list(my_dict)
            inlist = inlist[2:]
            for tests in inlist:
                test = my_dict.get(tests)[0]
                test1 = tests.split("-")
                if int(test1[0]) == x:
                    setattr(tb_male, tb_fields[counter_tb], Decimal(test))

        if sheet.cell_value(x, 2) != '':
            setattr(tb_female, tb_fields[counter_tb], sheet.cell_value(x, 2) or 0)
        else:
            inlist = list(my_dict)
            inlist = inlist[2:]
            for tests in inlist:
                test = my_dict.get(tests)[0]
                test1 = tests.split("-")
                if int(test1[0]) == x:
                    setattr(tb_female, tb_fields[counter_tb], Decimal(test))
        counter_tb = counter_tb + 1

    tb_male.save()
    tb_female.save()

    # schistosomiasis
    schisto_fields = misc.get_fields(Schistosomiasis)[1:3]
    schisto_male = Schistosomiasis(fhsis=fhsis, sex=Sex.objects.get(name='Male'))
    schisto_female = Schistosomiasis(fhsis=fhsis, sex=Sex.objects.get(name='Female'))
    sc_counter = 0

    for x in range(36, 38):
        if sheet.cell_value(x, 1) != '':
            setattr(schisto_male, schisto_fields[sc_counter], sheet.cell_value(x, 1) or 0)
        else:
            inlist = list(my_dict)
            inlist = inlist[2:]
            for tests in inlist:
                test = my_dict.get(tests)[0]
                test1 = tests.split("-")
                if int(test1[0]) == x:
                    setattr(schisto_male, schisto_fields[sc_counter], Decimal(test))

        if sheet.cell_value(x, 2) != '':
            setattr(schisto_female, schisto_fields[sc_counter], sheet.cell_value(x, 2) or 0)
        else:
            inlist = list(my_dict)
            inlist = inlist[2:]
            for tests in inlist:
                test = my_dict.get(tests)[0]
                test1 = tests.split("-")
                if int(test1[0]) == x:
                    setattr(schisto_female, schisto_fields[sc_counter], Decimal(test))
        sc_counter = sc_counter + 1

    schisto_male.save()
    schisto_female.save()

    # flariasis

    flariasis_fields = misc.get_fields(Flariasis)[1:4]
    flariasis_male = Flariasis(fhsis=fhsis, sex=Sex.objects.get(name='Male'))
    flariasis_female = Flariasis(fhsis=fhsis, sex=Sex.objects.get(name='Female'))
    flariasis_counter = 0

    for x in range(40, 43):
        if sheet.cell_value(x, 1) != '':
            setattr(flariasis_male, flariasis_fields[flariasis_counter], sheet.cell_value(x, 1) or 0)
        else:
            inlist = list(my_dict)
            inlist = inlist[2:]
            for tests in inlist:
                test = my_dict.get(tests)[0]
                test1 = tests.split("-")
                if int(test1[0]) == x:
                    setattr(flariasis_male, flariasis_fields[flariasis_counter], Decimal(test))

        if sheet.cell_value(x, 2) != '':
            setattr(flariasis_female, flariasis_fields[flariasis_counter], sheet.cell_value(x, 2) or 0)
        else:
            inlist = list(my_dict)
            inlist = inlist[2:]
            for tests in inlist:
                test = my_dict.get(tests)[0]
                test1 = tests.split("-")
                if int(test1[0]) == x:
                    setattr(flariasis_female, flariasis_fields[flariasis_counter], Decimal(test))
        flariasis_counter = flariasis_counter + 1

    flariasis_male.save()
    flariasis_female.save()

    # leprosy

    leprosy_fields = misc.get_fields(Leprosy)[1:3]
    leprosy_male = Leprosy(fhsis=fhsis, sex=Sex.objects.get(name='Male'))
    leprosy_female = Leprosy(fhsis=fhsis, sex=Sex.objects.get(name='Female'))
    leprosy_counter = 0

    for x in range(49, 61):
        if sheet.cell_value(x, 1) != '':
            setattr(leprosy_male, leprosy_fields[leprosy_counter], sheet.cell_value(x, 1) or 0)
        else:
            inlist = list(my_dict)
            inlist = inlist[2:]
            for tests in inlist:
                test = my_dict.get(tests)[0]
                test1 = tests.split("-")
                if int(test1[0]) == x:
                    setattr(leprosy_male, leprosy_fields[leprosy_counter], Decimal(test))

        if sheet.cell_value(x, 2) != '':
            setattr(leprosy_female, leprosy_fields[leprosy_counter], sheet.cell_value(x, 2) or 0)
        else:
            inlist = list(my_dict)
            inlist = inlist[2:]
            for tests in inlist:
                test = my_dict.get(tests)[0]
                test1 = tests.split("-")
                if int(test1[0]) == x:
                    setattr(leprosy_female, leprosy_fields[leprosy_counter], Decimal(test))
        leprosy_counter = leprosy_counter + 1

    leprosy_male.save()
    leprosy_female.save()

    # child care
    child_care_fields = misc.get_fields(ChildCare)[1:13]
    child_care_male = ChildCare(fhsis=fhsis, sex=Sex.objects.get(name='Male'))
    child_care_female = ChildCare(fhsis=fhsis, sex=Sex.objects.get(name='Female'))
    child_care_counter = 0

    for x in range(49, 61):
        if sheet.cell_value(x, 1) != '':
            setattr(child_care_male, child_care_fields[child_care_counter], sheet.cell_value(x, 1) or 0)
        else:
            inlist = list(my_dict)
            inlist = inlist[2:]
            for tests in inlist:
                test = my_dict.get(tests)[0]
                test1 = tests.split("-")
                if int(test1[0]) == x:
                    setattr(child_care_male, child_care_fields[child_care_counter], Decimal(test))

        if sheet.cell_value(x, 2) != '':
            setattr(child_care_female, child_care_fields[child_care_counter], sheet.cell_value(x, 2) or 0)
        else:
            inlist = list(my_dict)
            inlist = inlist[2:]
            for tests in inlist:
                test = my_dict.get(tests)[0]
                test1 = tests.split("-")
                if int(test1[0]) == x:
                    setattr(child_care_female, child_care_fields[child_care_counter], Decimal(test))

        child_care_counter = child_care_counter + 1

    child_care_male.save()
    child_care_female.save()

    messages.success(request, 'You have successfully uploaded the report')
    return redirect('core:bns-index')


@login_required
def display_fhsis(request, id):

    fhsis = FHSIS.objects.get(id=id)

    maternal = MaternalCare.objects.filter(fhsis=fhsis)
    immunization_female = Immunization.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Female'))
    immunization_male = Immunization.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Male'))

    malaria_female = Malaria.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Female'))
    malaria_male = Malaria.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Male'))

    tb_female = Tuberculosis.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Female'))
    tb_male = Tuberculosis.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Male'))

    schisto_female = Schistosomiasis.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Female'))
    schisto_male = Schistosomiasis.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Male'))

    flariasis_female = Flariasis.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Female'))
    flariasis_male = Flariasis.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Male'))

    leprosy_female = Leprosy.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Female'))
    leprosy_male = Leprosy.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Male'))

    child_care_female = ChildCare.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Female'))
    child_care_male = ChildCare.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Male'))

    sti = STISurveillance.objects.filter(fhsis=fhsis)

    profile = Profile.objects.get(user=request.user)

    context = {
        'profile': profile,
        'active': 'fh',
        'maternal': maternal,
        'immunization_female': immunization_female,
        'immunization_male': immunization_male,
        'malaria_female': malaria_female,
        'malaria_male': malaria_male,
        'tb_female': tb_female,
        'tb_male': tb_male,
        'schisto_female': schisto_female,
        'schisto_male': schisto_male,
        'flariasis_female': flariasis_female,
        'flariasis_male': flariasis_male,
        'leprosy_female': leprosy_female,
        'leprosy_male': leprosy_male,
        'child_care_female': child_care_female,
        'child_care_male': child_care_male,
        'sti': sti,
        'fhsis':fhsis
    }

    return render(request, 'datainput/display_fhsis.html', context)


@login_required
def display_monthly(request, id):
    profile = Profile.objects.get(user=request.user)
    barangay = Profile.objects.get(user=request.user).barangay

    patients = Patient.objects.filter(barangay=barangay)
    patients_now = patients.filter(date_created__year=id)
    print(datetime.now().year)
    print(patients_now)

    request.session['active'] = 'mr'
    print(barangay)

    context = {
        'profile': profile,
        'active': 'mr',
        'patients': set(patients_now),
        'barangay': barangay,
        'id': id
    }

    return render(request, 'datainput/monthly_reweighing_index.html', context)


@login_required
def display_opt(request, id):

    opt = OperationTimbang.objects.get(id=id)
    opt_values = OPTValues.objects.filter(opt=opt)
    wfa_normal = {}
    wfa_ow = {}
    wfa_uw = {}
    wfa_suw = {}
    hfa_normal = {}
    hfa_tall = {}
    hfa_stunted = {}
    hfa_ss = {}
    wfh_normal = {}
    wfh_ow = {}
    wfh_obese = {}
    wfh_wasted = {}
    wfh_sw = {}

    def append_values(category, dict_name):
        for value in category:
            age_group = value.age_group

            if age_group.name == "0 to 5 months old":
                if age_group.sex.name == "Male":
                    dict_name["Male - 0 to 5 months old"] = value
                elif age_group.sex.name == "Female":
                    dict_name["Female - 0 to 5 months old"] = value

            if age_group.name == "6 to 11 months old":
                if age_group.sex.name == "Male":
                    dict_name["Male - 6 to 11 months old"] = value
                elif age_group.sex.name == "Female":
                    dict_name["Female - 6 to 11 months old"] = value

            if age_group.name == "12 to 23 months old":
                if age_group.sex.name == "Male":
                    dict_name["Male - 12 to 23 months old"] = value
                elif age_group.sex.name == "Female":
                    dict_name["Female - 12 to 23 months old"] = value

            if age_group.name == "24 to 35 months old":
                if age_group.sex.name == "Male":
                    dict_name["Male - 24 to 35 months old"] = value
                elif age_group.sex.name == "Female":
                    dict_name["Female - 24 to 35 months old"] = value

            if age_group.name == "36 to 47 months old":
                if age_group.sex.name == "Male":
                    dict_name["Male - 36 to 37 months old"] = value
                elif age_group.sex.name == "Female":
                    dict_name["Female - 36 to 47 months old"] = value

            if age_group.name == "48 to 59 months old":
                if age_group.sex.name == "Male":
                    dict_name["Male - 48 to 59 months old"] = value
                elif age_group.sex.name == "Female":
                    dict_name["Female - 48 to 59 months old"] = value

            if age_group.name == "60 to 71 months old":
                if age_group.sex.name == "Male":
                    dict_name["Male - 60 to 71 months old"] = value
                elif age_group.sex.name == "Female":
                    dict_name["Female - 60 to 71 months old"] = value
                    print(value.age_group, value.values)

    # Weight for Age -- Normal
    opt_values_wfa_normal = opt_values.filter(nutritional_status=NutritionalStatus.objects.get(name="Weight for Age - Normal"))
    append_values(opt_values_wfa_normal, wfa_normal)

    # Weight for Age -- Overweight
    opt_values_wfa_ow = opt_values.filter(nutritional_status=NutritionalStatus.objects.get(name="Weight for Age - Overweight"))
    append_values(opt_values_wfa_ow, wfa_ow)

    # Weight for Age - Underweight
    opt_values_wfa_uw = opt_values.filter(nutritional_status=NutritionalStatus.objects.get(name="Weight for Age - Underweight"))
    append_values(opt_values_wfa_uw, wfa_uw)

    # Weight for Age - Severely Underweight
    opt_values_wfa_suw = opt_values.filter(nutritional_status=NutritionalStatus.objects.get(name="Weight for Age - Severely Underweight"))
    append_values(opt_values_wfa_suw, wfa_suw)

    # Height for Age - Normal
    opt_values_hfa_normal = opt_values.filter(nutritional_status=NutritionalStatus.objects.get(name="Height for Age - Normal"))
    append_values(opt_values_hfa_normal, hfa_normal)

    # Height for Age - Tall
    opt_values_hfa_tall = opt_values.filter(nutritional_status=NutritionalStatus.objects.get(name="Height for Age - Tall"))
    append_values(opt_values_hfa_tall, hfa_tall)

    # Height for Age - Stunted
    opt_values_hfa_stunted = opt_values.filter(nutritional_status=NutritionalStatus.objects.get(name="Height for Age - Stunted"))
    append_values(opt_values_hfa_stunted, hfa_stunted)

    # Height for Age - Severely Stunted
    opt_values_hfa_ss = opt_values.filter(nutritional_status=NutritionalStatus.objects.get(name="Height for Age - Severely Stunted"))
    append_values(opt_values_hfa_ss, hfa_ss)

    # Weight for Height - Normal
    opt_values_wfh_normal = opt_values.filter(nutritional_status=NutritionalStatus.objects.get(name="Weight for Height/Length - Normal"))
    append_values(opt_values_wfh_normal, wfh_normal)

    # Weight for Height - Overweight
    opt_values_wfh_ow = opt_values.filter(nutritional_status=NutritionalStatus.objects.get(name="Weight for Height/Length - Overweight"))
    append_values(opt_values_wfh_ow, wfh_ow)

    # Weight for Height - Obese
    opt_values_wfh_obese = opt_values.filter(nutritional_status=NutritionalStatus.objects.get(name="Weight for Height/Length - Obese"))
    append_values(opt_values_wfh_obese, wfh_obese)

    # Weight for Height - Wasted
    opt_values_wfh_wasted = opt_values.filter(nutritional_status=NutritionalStatus.objects.get(name="Weight for Height/Length - Wasted"))
    append_values(opt_values_wfh_wasted, wfh_wasted)

    # Weight for Height - Severely Wasted
    opt_values_wfh_sw = opt_values.filter(nutritional_status=NutritionalStatus.objects.get(name="Weight for Height/Length - Severely Wasted"))
    append_values(opt_values_wfh_sw, wfh_sw)

    profile = Profile.objects.get(user=request.user)

    context = {
        'profile': profile,
        'wfa_normal': wfa_normal,
        'wfa_ow': wfa_ow,
        'wfa_uw': wfa_uw,
        'wfa_suw': wfa_suw,
        'hfa_normal': hfa_normal,
        'hfa_tall': hfa_normal,
        'hfa_stunted': hfa_stunted,
        'hfa_ss': hfa_ss,
        'wfh_normal': wfh_normal,
        'wfh_ow': wfh_ow,
        'wfh_obese': wfh_obese,
        'wfh_wasted': wfh_wasted,
        'wfh_sw': wfh_sw,
        'opt':opt,
        'active':'ot'
    }

    return render(request, 'datainput/display_opt.html', context)


@login_required
def barangay_archives(request):

    context = {
        'barangays': Barangay.objects.all()
    }

    return render(request, 'datainput/nutritionist_barangay_archives.html', context)


@login_required
def latest_opt(request):

    profile = Profile.objects.get(user=request.user)

    opt = OperationTimbang.objects.filter(barangay=profile.barangay).latest('id')

    opt_values = OPTValues.objects.filter(opt=opt)
    wfa_normal = {}
    wfa_ow = {}
    wfa_uw = {}
    wfa_suw = {}
    hfa_normal = {}
    hfa_tall = {}
    hfa_stunted = {}
    hfa_ss = {}
    wfh_normal = {}
    wfh_ow = {}
    wfh_obese = {}
    wfh_wasted = {}
    wfh_sw = {}

    def append_values(category, dict_name):
        for value in category:
            age_group = value.age_group

            if age_group.name == "0 to 5 months old":
                if age_group.sex.name == "Male":
                    dict_name["Male - 0 to 5 months old"] = value
                elif age_group.sex.name == "Female":
                    dict_name["Female - 0 to 5 months old"] = value

            if age_group.name == "6 to 11 months old":
                if age_group.sex.name == "Male":
                    dict_name["Male - 6 to 11 months old"] = value
                elif age_group.sex.name == "Female":
                    dict_name["Female - 6 to 11 months old"] = value

            if age_group.name == "12 to 23 months old":
                if age_group.sex.name == "Male":
                    dict_name["Male - 12 to 23 months old"] = value
                elif age_group.sex.name == "Female":
                    dict_name["Female - 12 to 23 months old"] = value

            if age_group.name == "24 to 35 months old":
                if age_group.sex.name == "Male":
                    dict_name["Male - 24 to 35 months old"] = value
                elif age_group.sex.name == "Female":
                    dict_name["Female - 24 to 35 months old"] = value

            if age_group.name == "36 to 47 months old":
                if age_group.sex.name == "Male":
                    dict_name["Male - 36 to 37 months old"] = value
                elif age_group.sex.name == "Female":
                    dict_name["Female - 36 to 47 months old"] = value

            if age_group.name == "48 to 59 months old":
                if age_group.sex.name == "Male":
                    dict_name["Male - 48 to 59 months old"] = value
                elif age_group.sex.name == "Female":
                    dict_name["Female - 48 to 59 months old"] = value

            if age_group.name == "60 to 71 months old":
                if age_group.sex.name == "Male":
                    dict_name["Male - 60 to 71 months old"] = value
                elif age_group.sex.name == "Female":
                    dict_name["Female - 60 to 71 months old"] = value

    # Weight for Age -- Normal
    opt_values_wfa_normal = opt_values.filter(nutritional_status=NutritionalStatus.objects.get(name="Weight for Age - Normal"))
    append_values(opt_values_wfa_normal, wfa_normal)

    # Weight for Age -- Overweight
    opt_values_wfa_ow = opt_values.filter(nutritional_status=NutritionalStatus.objects.get(name="Weight for Age - Overweight"))
    append_values(opt_values_wfa_ow, wfa_ow)

    # Weight for Age - Underweight
    opt_values_wfa_uw = opt_values.filter(nutritional_status=NutritionalStatus.objects.get(name="Weight for Age - Underweight"))
    append_values(opt_values_wfa_uw, wfa_uw)

    # Weight for Age - Severely Underweight
    opt_values_wfa_suw = opt_values.filter(nutritional_status=NutritionalStatus.objects.get(name="Weight for Age - Severely Underweight"))
    append_values(opt_values_wfa_suw, wfa_suw)

    # Height for Age - Normal
    opt_values_hfa_normal = opt_values.filter(nutritional_status=NutritionalStatus.objects.get(name="Height for Age - Normal"))
    append_values(opt_values_hfa_normal, hfa_normal)

    # Height for Age - Tall
    opt_values_hfa_tall = opt_values.filter(nutritional_status=NutritionalStatus.objects.get(name="Height for Age - Tall"))
    append_values(opt_values_hfa_tall, hfa_tall)

    # Height for Age - Stunted
    opt_values_hfa_stunted = opt_values.filter(nutritional_status=NutritionalStatus.objects.get(name="Height for Age - Stunted"))
    append_values(opt_values_hfa_stunted, hfa_stunted)

    # Height for Age - Severely Stunted
    opt_values_hfa_ss = opt_values.filter(nutritional_status=NutritionalStatus.objects.get(name="Height for Age - Severely Stunted"))
    append_values(opt_values_hfa_ss, hfa_ss)

    # Weight for Height - Normal
    opt_values_wfh_normal = opt_values.filter(nutritional_status=NutritionalStatus.objects.get(name="Weight for Height/Length - Normal"))
    append_values(opt_values_wfh_normal, wfh_normal)

    # Weight for Height - Overweight
    opt_values_wfh_ow = opt_values.filter(nutritional_status=NutritionalStatus.objects.get(name="Weight for Height/Length - Overweight"))
    append_values(opt_values_wfh_ow, wfh_ow)

    # Weight for Height - Obese
    opt_values_wfh_obese = opt_values.filter(nutritional_status=NutritionalStatus.objects.get(name="Weight for Height/Length - Obese"))
    append_values(opt_values_wfh_obese, wfh_obese)

    # Weight for Height - Wasted
    opt_values_wfh_wasted = opt_values.filter(nutritional_status=NutritionalStatus.objects.get(name="Weight for Height/Length - Wasted"))
    append_values(opt_values_wfh_wasted, wfh_wasted)

    # Weight for Height - Severely Wasted
    opt_values_wfh_sw = opt_values.filter(nutritional_status=NutritionalStatus.objects.get(name="Weight for Height/Length - Severely Wasted"))
    append_values(opt_values_wfh_sw, wfh_sw)

    context = {
        'wfa_normal': wfa_normal,
        'wfa_ow': wfa_ow,
        'wfa_uw': wfa_uw,
        'wfa_suw': wfa_suw,
        'hfa_normal': hfa_normal,
        'hfa_tall': hfa_normal,
        'hfa_stunted': hfa_stunted,
        'hfa_ss': hfa_ss,
        'wfh_normal': wfh_normal,
        'wfh_ow': wfh_ow,
        'wfh_obese': wfh_obese,
        'wfh_wasted': wfh_wasted,
        'wfh_sw': wfh_sw,
        'opt':opt,
        'profile':profile,
        'active': 'uf'
    }

    return render(request, 'datainput/display_opt.html', context)


@login_required
def latest_fhsis(request):

    profile = Profile.objects.get(user=request.user)

    fhsis = FHSIS.objects.filter(barangay=profile.barangay).latest('id')

    maternal = MaternalCare.objects.filter(fhsis=fhsis)
    immunization_female = Immunization.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Female'))
    immunization_male = Immunization.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Male'))

    malaria_female = Malaria.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Female'))
    malaria_male = Malaria.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Male'))

    tb_female = Tuberculosis.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Female'))
    tb_male = Tuberculosis.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Male'))

    schisto_female = Schistosomiasis.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Female'))
    schisto_male = Schistosomiasis.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Male'))

    flariasis_female = Flariasis.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Female'))
    flariasis_male = Flariasis.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Male'))

    leprosy_female = Leprosy.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Female'))
    leprosy_male = Leprosy.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Male'))

    child_care_female = ChildCare.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Female'))
    child_care_male = ChildCare.objects.filter(fhsis=fhsis, sex=Sex.objects.get(name='Male'))

    sti = STISurveillance.objects.filter(fhsis=fhsis)



    context = {
        'profile': profile,
        'active': 'uf',
        'maternal': maternal,
        'immunization_female': immunization_female,
        'immunization_male': immunization_male,
        'malaria_female': malaria_female,
        'malaria_male': malaria_male,
        'tb_female': tb_female,
        'tb_male': tb_male,
        'schisto_female': schisto_female,
        'schisto_male': schisto_male,
        'flariasis_female': flariasis_female,
        'flariasis_male': flariasis_male,
        'leprosy_female': leprosy_female,
        'leprosy_male': leprosy_male,
        'child_care_female': child_care_female,
        'child_care_male': child_care_male,
        'sti': sti,
        'fhsis':fhsis
    }

    return render(request, 'datainput/display_fhsis.html', context)


@login_required
def select_report_nutritionist(request):

    report = request.POST['report']
    barangay = request.POST['barangay']

    context = {

    }

    if report == 'fhsis':
        context['records'] = FHSIS.objects.filter(barangay_id=barangay)
        return render(request, 'datainput/archives_nutritionist/fhsis_records.html', context)

    elif report == 'mr':
        context['records'] = Patient.objects.filter(barangay_id=barangay)
        return render(request, 'datainput/archives_nutritionist/reweighing_records.html', context)

    elif report == 'opt':
        context['records'] = OperationTimbang.objects.filter(barangay_id=barangay)
        return render(request, 'datainput/archives_nutritionist/opt_records.html', context)

    elif report == 'fp':
        context['records'] = FamilyProfile.objects.filter(barangay_id=barangay)
        return render(request, 'datainput/archives_nutritionist/family_records.html', context)


@login_required
def populate_eopt(request):
    path = "/Users/kamillegamboa/Documents/GitHub/Likha-Capstone/capstone/files/OPTValuesExcelVer2.xls"
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_index(0)

# 23661
#

    for x in range(2, 4733):
        for n in range(0, 3+1):
            if n == 0:
                opt = OperationTimbang.objects.get(id=sheet.cell_value(x, n))
            if n == 1:
                values = sheet.cell_value(x, n)
            if n == 2:
                nutritional_status = NutritionalStatus.objects.get(id=sheet.cell_value(x, n))
            if n == 3:
                age_group = AgeGroup.objects.get(id=sheet.cell_value(x, n))

        new_opt_value_instance = OPTValues.objects.create(opt=opt, values=values,
                                                          nutritional_status=nutritional_status, age_group=age_group)

    return HttpResponse("success")
    # date1 = date(2013, 3, 31)
    # barangays = Barangay.objects.all()
    # profile = Profile.objects.get(user=request.user)
    # for b in barangays:
    #     OperationTimbang.objects.create(date=date1, barangay=b, uploaded_by=profile)


@login_required
def notify_bns(request):

    barangay = request.POST.get('barangay')
    sender = Profile.objects.get(user=request.user)

    message = 'Please upload the reports as soon as possible.'

    for user in Barangay.objects.get(id=barangay.id).profile_set.all():

        Notification.objects.create(
            message=message,
            profile_to=user,
            profile_from=sender
        )

    messages.success(request, 'Users successfully notified')


@login_required
def notify(request, barangay_name, report):

    barangay = Barangay.objects.get(name=barangay_name)

    sender = Profile.objects.get(user=request.user)
    message = 'Please upload your %s report as soon as possible. Flagged by %s' % (report, sender.user.username)

    for p in Profile.objects.filter(barangay=barangay):
        Notification.objects.create(
            message=message,
            profile_to=p,
            profile_from=sender
        )

    messages.success(request, 'Users successfully notified')
    return redirect('core:nutritionist')



