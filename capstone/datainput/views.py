
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
from datainput.forms import FamilyProfileForm, PatientForm, MonthlyReweighingForm, HealthCareWasteManagementForm, \
    InformalSettlersForm, UnemploymentRateForm
from friends.datainput import excel_uploads, validations
from core.models import Profile, Notification
from datainput.models import OperationTimbang, NutritionalStatus, AgeGroup, OPTValues, FamilyProfile, FamilyProfileLine, \
    Patient, MonthlyReweighing, HealthCareWasteManagement, InformalSettlers, UnemploymentRate, Barangay


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
        profile = Profile.objects.get(user=request.user)

        if check.count() == 0:
            family_profile = FamilyProfile.objects.create(barangay=barangay, status='Pending', uploaded_by=profile)

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
    profile = Profile.objects.get(user=request.user)

    context = {
        'profile': profile,
        'patients': patients,
        'has_opt': len(opt) > 0,
        'barangay': barangay
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
    profile = Profile.objects.get(user=request.user)

    context = {
        'patient': patient,
        'weights': weights,
        'is_bns': profile.user_type == 'Barangay Nutrition Scholar'
    }

    return render(request, 'datainput/patient_overview.html', context)


@login_required
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

    context = {
        'form': form
    }

    return render(request, 'datainput/monthly_reweighing_form.html', context)


@login_required
def nutritionist_upload(request):

    has_health_care = validations.has_health_care()
    has_informal = validations.has_informal_settlers()
    has_ur = validations.has_unemployment_rate()

    context = {
        'has_health_care': has_health_care,
        'has_informal': has_informal,
        'has_ur': has_ur
    }

    return render(request, 'datainput/nutritionist_upload.html', context)


@login_required
def health_care_waste_management_index(request):

    hcwm = HealthCareWasteManagement.objects.all()

    context = {
        'hcwm': hcwm,
    }

    return render(request, 'datainput/hcwm_index.html', context)


@login_required
def add_hcwm(request):

    if validations.has_health_care():

        messages.error(request, 'Record for this year has already been uploaded')
        return redirect('datainput:health_care_index')

    form = HealthCareWasteManagementForm(request.POST or None)

    context = {
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

    context = {
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

    context = {
        'form': form,
        'records': records,
        'has_record': validations.has_unemployment_rate()
    }

    return render(request, 'datainput/unemployment_rate.html', context)


# data status index
@login_required
def data_status_index(request):

    barangays = Barangay.objects.all()

    context = {
        'barangays': barangays
    }

    return render(request, 'datainput/data_status_index.html', context)


@login_required
def show_opt(request, id):

    barangay = Barangay.objects.get(id=id)

    opt = OperationTimbang.objects.filter(barangay=barangay)

    context = {
        'opt': opt,
        'barangay': barangay,
    }

    return render(request, 'datainput/show_opt.html', context)


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
def view_reweighing(request, id):

    barangay = Barangay.objects.get(id=id)
    opt = OperationTimbang.objects.filter(barangay=barangay, date__year=datetime.now().year)
    patients = Patient.objects.filter(barangay=barangay)

    context = {
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

    context = {
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












