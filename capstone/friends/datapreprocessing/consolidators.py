from datetime import datetime

from django.apps import apps

from datainput.models import HealthCareWasteManagement, OPTValues, UnemploymentRate, InformalSettlers, Sex, \
    NutritionalStatus, MonthlyReweighing


def get_value(metric):

    phrase = metric.split("|")

    # get model
    str_model = get_model(metric)
    model = apps.get_model('datainput', str_model)
    print(get_reweighing_counts())

    # get field
    # not applicable for NutritionalStatuses

    if str_model == 'OPTValues':
        status = NutritionalStatus.objects.get(name=phrase[1].strip())
        sex = Sex.objects.get(name=phrase[2].strip())
        return get_total_opt(status, sex)

    elif str_model == 'HealthCareWasteManagement':
        field = get_field(model, phrase[1])
        return get_total_hcwm(field)

    elif str_model == 'InformalSettlers':
        return get_informal_settlers()

    elif str_model == 'UnemploymentRate':
        return UnemploymentRate.objects.filter(date__year=datetime.now().year)[0].rate

    elif str_model == 'MaternalCare' or str_model == 'STISurveillance':
        field = get_field(model, phrase[1])
        return get_maternal_or_sti(model, field)

    elif str_model == 'Immunization' or str_model == 'Malaria' or str_model == 'Tuberculosis' or str_model == 'Schistosomiasis' \
        or str_model == 'Flariasis' or str_model == 'Leprosy' or str_model == 'ChildCare':

        field = get_field(model, phrase[1])
        return get_total_with_sex(model, field, sex=Sex.objects.get(name=phrase[2].strip()))

    return 0


def get_model(metric):

    phrase = metric.split("|")
    model = 'default'
    first = phrase[0]

    if len(phrase) == 2:

        if 'Maternal Care' in first:
            model = 'MaternalCare'
        elif 'STI Surveillance' in first:
            model = 'STISurveillance'
        elif 'Family Profile' in first:
            model = 'FamilyProfileLine'
        elif 'Health Care Waste Management' in first:
            model = 'HealthCareWasteManagement'
        elif 'Informal Settlers' in first:
            model = 'InformalSettlers'

    elif len(phrase) == 1:

        if 'Unemployment Rate' in first:
            model = 'UnemploymentRate'

    elif len(phrase) == 3:

        if 'Nutritional Status' in first:
            return 'OPTValues'
        else:
            return first.replace(' ', '')

    return model


def get_field(model, verbose):

    if not model is OPTValues:
        fields = []
        for field in model._meta.get_fields():
            if field.verbose_name == verbose.strip():
                fields.append(field)

        str_field =  str(fields[0]).split(".")
        return str_field[2]

    return None


def get_total_hcwm(field):

    count = 0
    records = HealthCareWasteManagement.objects.filter(date__year=datetime.now().year)

    for record in records:
        count = count + getattr(record, field)

    return count


def get_informal_settlers():

    count = 0
    for record in InformalSettlers.objects.filter(date__year=datetime.now().year):
        count = count + getattr(record, 'families_count')

    return count


# fhsis
def get_maternal_or_sti(model, field):

    records = model.objects.all().filter(fhsis__date__year=datetime.now().year)

    count = 0
    for record in records:
        count = count + getattr(record, field)

    return count


def get_total_with_sex(model, field, sex):

    records = model.objects.all().filter(fhsis__date__year=datetime.now().year, sex=sex)
    count = 0
    print(records)

    for record in records:
        count = count + getattr(record, field)

    return count


# NOTE: sex should be the string form and not the model
def get_total_opt(status, sex):

    records = OPTValues.objects.filter(opt__date__year=datetime.now().year,
                                       nutritional_status=status,
                                       age_group__sex=sex)

    count = 0
    for record in records:
        count = count + record.values

    return count


def get_reweighing_counts(status=None, sex=None):

    labels =  MonthlyReweighing._meta.get_fields()[2:5]
    labels = [
        'Weight for Age',
        'Height for Age',
        'Weight for Height/Length'
    ]

    records = MonthlyReweighing.objects.filter(date__year=datetime.now().year)

    # status = 'Weight for Age - Overweight'

    count = 0
    for record in records:

        if status in record.get_nutritional_status() and record.patient.sex == sex:
            count = count + 1

    return count

