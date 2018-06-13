from datetime import datetime

from datainput.models import NutritionalStatus, OPTValues, MonthlyReweighing, OperationTimbang

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

    return count


# get reweighing weights
def get_weights_reweighing(status, sex, month):

    records = MonthlyReweighing.objects.filter(date__month=month, patient__sex=sex)
    count = 0

    for record in records:
        if status in record.get_nutritional_status():
            count = count + 1

    return count


def get_weight_values_per_month(status, sex):

    month = OperationTimbang.objects.filter(date__year=datetime.now().year)[0].date.month

    values = {
        month: get_weights_opt(status, sex, datetime.now().year)
    }

    return values



