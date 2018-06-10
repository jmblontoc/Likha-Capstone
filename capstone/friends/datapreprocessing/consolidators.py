from django.apps import apps

def get_value(metric):

    # check if may hyphen

    phrase = metric.split("|")

    # get model
    model = apps.get_model('datainput', get_model(metric))
    print(model)

    # get field
    x = model._meta.get_field(verbose_name=phrase[1])
    print(x)

    # args = is yearly, is monthly, is barangay level,

    return len(phrase)


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

    elif len(phrase) == 1:

        if 'Unemployment Rate' in first:
            model = 'UnemploymentRate'
        elif 'Informal Settlers' in first:
            model = 'InformalSettlers'

    elif len(phrase) == 3:

        if 'Nutritional Status' in first:
            return 'OPTValues'
        else:
            return first.replace(' ', '')

    return model


def get_total(model, field):
    pass
