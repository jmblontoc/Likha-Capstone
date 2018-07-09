from datetime import datetime

from django.db.models import Sum

from friends import datapoints
from django.apps import apps

from datainput.models import HealthCareWasteManagement, OPTValues, UnemploymentRate, InformalSettlers, Sex, \
    NutritionalStatus, MonthlyReweighing, FamilyProfileLine


def get_value(metric):

    phrase = metric.split("|")

    # get model
    str_model = get_model(metric)
    model = apps.get_model('datainput', str_model)

    # get field
    # not applicable for NutritionalStatuses

    if str_model == 'OPTValues':

        status = NutritionalStatus.objects.get(name=phrase[1].strip())

        if len(phrase) == 2:

            opt = get_total_opt_no_sex(status)
            reweighing = get_reweighing_no_sex(str(status))

            return opt # + reweighing

        sex = Sex.objects.get(name=phrase[2].strip())
        opt = get_total_opt(status, sex)
        reweighing = get_reweighing_counts(phrase[1].strip(), sex)
        # print(reweighing)

        return opt + reweighing

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
        if len(phrase) == 2:
            return get_total_without_sex(model, field)

        return get_total_with_sex(model, field, sex=Sex.objects.get(name=phrase[2].strip()))

    elif str_model == 'FamilyProfileLine':
        try:
            field = get_field(model, phrase[1])
            if field in datapoints.main_family_profile:
                return get_population(field)

            if field in datapoints.boolean_fields_fp:
                return get_boolean_totals(field)
        except IndexError:
            field = get_field_choices(phrase[1].strip())
            return get_choice_count(field, phrase[1].strip())

        return 123123

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
        elif 'Nutritional Status' in first:
            return 'OPTValues'
        elif 'Child Care' in first:
            return 'ChildCare'

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
            if field.verbose_name.strip() == verbose.strip():
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

    for record in records:

        try:
            count = count + getattr(record, field)
        except TypeError:
            print('aha')

    return count


def get_total_without_sex(model, field):

    records = model.objects.all().filter(fhsis__date__year=datetime.now().year)
    count = 0

    for record in records:

        try:
            count = count + getattr(record, field)
        except TypeError:
            print('aha')

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


# opt total without sex
def get_total_opt_no_sex(status):

    return OPTValues.objects.filter(opt__date__year=datetime.now().year,
                                    nutritional_status=status).aggregate(sum=Sum('values'))['sum']


# KAMMY YOU CAN USE THIS METHOD
def get_reweighing_no_sex(status):
    records = MonthlyReweighing.objects.filter(date__year=datetime.now().year, date__month=datetime.now().month)

    # status = 'Weight for Age - Overweight'
    count = 0
    for record in records:

        if status in record.get_nutritional_status():
            count = count + 1

    return count


def get_total_opt_date(status, sex, start_date, end_date):

    records = OPTValues.objects.filter(nutritional_status=status, age_group__sex=sex, opt__date__range=[
        start_date, end_date
    ])

    if records.count() == 0:
        return 0

    return records.aggregate(sum=Sum('values'))['sum']


# THIS IS WITH SEX
def get_reweighing_counts(status, sex):

    records = MonthlyReweighing.objects.filter(date__year=datetime.now().year, patient__sex=sex)

    # status = 'Weight for Age - Overweight'
    count = 0
    for record in records:

        if status in record.get_nutritional_status():
            count = count + 1

    return count


def get_reweighing_counts_date(status, sex, start_date, end_date):

    records = MonthlyReweighing.objects.filter(
        patient__sex=sex,
        date__range=[start_date, end_date]
    )

    count = 0
    for record in records:
        if status in record.get_nutritional_status():
            count = count + 1

    return count

# for family profiles
def get_field_choices(field):

    if field in datapoints.educational_attainment:
        return 'educational_attainment'
    elif field in datapoints.toilet_type:
        return 'toilet_type'
    elif field in datapoints.water_sources:
        return 'water_sources'
    elif field in datapoints.food_production:
        return 'food_production_activity'
    else:
        return 'wala'


def get_choice_count(field, choice):

    count = 0
    records = FamilyProfileLine.objects.filter(family_profile__date__year=datetime.now().year)

    for record in records:
        if getattr(record, field) == choice:
            count = count + 1

    return count


# population
def get_population(field):

    records  = FamilyProfileLine.objects.filter(family_profile__date__year=datetime.now().year)

    total = 0
    for record in records:

        count = getattr(record, field)
        total = total + count

    return total


def get_boolean_totals(field):

    records  = FamilyProfileLine.objects.filter(family_profile__date__year=datetime.now().year)

    total = 0
    for record in records:
        if getattr(record, field):
            total = total + 1

    return total