from datetime import datetime

from django.apps import apps

from datainput.models import HealthCareWasteManagement, OPTValues, UnemploymentRate


def get_value(metric):

    phrase = metric.split("|")

    # get model
    str_model = get_model(metric)
    model = apps.get_model('datainput', str_model)


    # get field
    # not applicable for NutritionalStatuses

    if str_model == 'OPTValues':
        print('todo')

    elif str_model == 'HealthCareWasteManagement':
        field = get_field(model, phrase[1])
        return get_total_count(model, field, True, False, False)

    elif str_model == 'InformalSettlers':
        field = get_field(model, phrase[1])
        return get_total_count(model, field, False, True, False)

    elif str_model == 'UnemploymentRate':
        return UnemploymentRate.objects.filter(date__year=datetime.now().year)[0].rate

    # args = is yearly, is monthly, is barangay level,

    return 'wait lang'


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


def get_total_count(model, field, is_annual, is_monthly, is_barangay):

    if is_annual:
        if not is_barangay:

            # health care waste management
            count = 0
            records = model.objects.all().filter(date__year=datetime.now().year)

            for record in records:
                count = count + getattr(record, field)

            return count

    else:
        if not is_barangay:

            # informal settlers
            count = 0
            records = model.objects.all().filter(date__year=datetime.now().year)

            for record in records:
                count = count + getattr(record, field)

            return count


