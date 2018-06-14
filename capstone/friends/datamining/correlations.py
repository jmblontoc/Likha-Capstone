
from datetime import datetime

from datainput.models import NutritionalStatus, OPTValues, MonthlyReweighing, OperationTimbang, MaternalCare, \
    STISurveillance

month_now = datetime.now().month
# get nutritional statuses

nutritional_statuses = NutritionalStatus.objects.all()

# get all data points


# get nutritional statuses by month


# get nutritional statuses by year

# get data points by month

# get data points by year

# # # # # # # # # # # # # # # # # # # # # # # # # #

# get opt weights per year
def get_weights_opt(status, sex, year):

    records = OPTValues.objects.filter(nutritional_status=status, age_group__sex=sex, opt__date__year=year)
    count = 0

    for record in records:
        count = count + record.values

    return float(count)


# get reweighing weights
def get_weights_reweighing(status, sex, month):

    records = MonthlyReweighing.objects.filter(date__month=month, patient__sex=sex)
    count = 0

    for record in records:
        if status.name in record.get_nutritional_status():
            count = count + 1

    return float(count)


def get_weight_values_per_month(status, sex):

    month = OperationTimbang.objects.filter(date__year=datetime.now().year)[0].date.month

    values = {
        month: get_weights_opt(status, sex, datetime.now().year)
    }

    while month < month_now:
        values[month + 1] = get_weights_reweighing(status, sex, month + 1)
        month = month + 1

    print(status)
    return values


# # # # # # # # DATA POINTS # # # # # # # # # #

# get starting month of the current year for FHSIS records ONLY
def get_starting_month(model):

    months = []
    records = model.objects.all().filter(fhsis__date__year=datetime.now().year)
    for record in records:
        months.append(record.fhsis.date.month)

    return min(months)


# maternal care
def get_maternal_care(field):

    start_month = get_starting_month(MaternalCare)
    base = MaternalCare.objects.filter(fhsis__date__year=datetime.now().year)

    values = {

    }

    while start_month <= month_now:

        count = 0
        records = base.filter(fhsis__date__month=start_month)

        for record in records:
            count = count + getattr(record, field)

        values[start_month] = count
        start_month = start_month + 1

    return values


# STISurveillance
def get_sti_surveillance(field):

    start_month = get_starting_month(STISurveillance)
    base = STISurveillance.objects.filter(fhsis__date__year=datetime.now().year)

    values = {

    }

    while start_month <= month_now:

        count = 0
        records = base.filter(fhsis__date__month=start_month)

        for record in records:
            count = count + getattr(record, field)

        values[start_month] = count
        start_month = start_month + 1

    return values

