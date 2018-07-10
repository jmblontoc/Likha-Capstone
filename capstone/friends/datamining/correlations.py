
from datetime import datetime

import numpy
from django.db.models import Sum
from computations import weights as w, child_care, maternal
from datainput.models import NutritionalStatus, OPTValues, MonthlyReweighing, OperationTimbang, MaternalCare, \
    STISurveillance, UnemploymentRate, InformalSettlers, Sex, Flariasis, Leprosy, Schistosomiasis, Immunization, \
    Malaria, Tuberculosis, ChildCare
from friends import  datapoints
import collections

month_now = datetime.now().month
year_now = datetime.now().year
# get nutritional statuses

nutritional_statuses = NutritionalStatus.objects.all()

# # # # # # # # # # # # # # # # # # # # # # # # # #


# get opt weights per year
def get_weights_opt(status, sex, year):

    if sex is None:
        return OPTValues.objects.filter(nutritional_status=status, opt__date__year=year).aggregate(sum=Sum('values'))['sum']

    records = OPTValues.objects.filter(nutritional_status=status, age_group__sex=sex, opt__date__year=year)
    count = 0

    for record in records:
        count = count + record.values

    return float(count)


# get reweighing weights
def get_weights_reweighing(status, sex, month):

    if sex is None:

        records = MonthlyReweighing.objects.filter(date__month=month)
        count = 0

        for record in records:
            if status.name in record.get_nutritional_status():
                count = count + 1

        return float(count)

    records = MonthlyReweighing.objects.filter(date__month=month, patient__sex=sex)
    count = 0

    for record in records:
        if status.name in record.get_nutritional_status():
            count = count + 1

    return float(count)


def get_weight_values():

    uw = NutritionalStatus.objects.get(name__contains='Weight for Age - Underweight')
    suw = NutritionalStatus.objects.get(name__contains='Weight for Age - Severely Underweight')
    month = OperationTimbang.objects.filter(date__year=datetime.now().year)[0].date.month

    values = {
        month: int(get_weights_opt(uw, None, year_now) + get_weights_opt(suw, None, year_now))
    }

    while month < month_now:
        values[month + 1] = get_weights_reweighing(uw, None, month + 1) + get_weights_reweighing(suw, None, month + 1)
        month = month + 1

    return values


def get_weight_values_per_month(status, sex):

    month = OperationTimbang.objects.filter(date__year=datetime.now().year)[0].date.month

    values = {
        month: get_weights_opt(status, sex, datetime.now().year)
    }

    while month < month_now:
        values[month + 1] = get_weights_reweighing(status, sex, month + 1)
        month = month + 1

    return values


# # # # # # # # DATA POINTS MONTHLY # # # # # # # # # #

# get starting month of the current year for FHSIS records ONLY
def get_starting_month(model):

    months = []
    records = model.objects.all().filter(fhsis__date__year=datetime.now().year)
    for record in records:
        months.append(record.fhsis.date.month)

    return min(months)


# similar but year
def get_starting_year(model):

    years = []
    records = model.objects.all()
    for record in records:
        years.append(record.date.year)

    return min(years)


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

        values[start_month] = int(count)
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


# FHSIS
def get_fhsis(model, field, sex):

    start_month = get_starting_month(model)

    if sex is None:
        base = model.objects.all().filter(fhsis__date__year=year_now)
    else:
        base = model.objects.all().filter(fhsis__date__year=datetime.now().year, sex=sex)

    values = {

    }

    while start_month <= month_now:

        count = 0
        records = base.filter(fhsis__date__month=start_month)

        for record in records:
            try:
                count = count + getattr(record, field)
            except TypeError:
                pass

        values[start_month] = float(count)
        start_month = start_month + 1

    return values


def get_fhsis_no_sex(model, field):

    start_month = get_starting_month(model)
    base = model.objects.all().filter(fhsis__date__year=datetime.now().year)

    values = {

    }

    while start_month <= month_now:

        count = 0
        records = base.filter(fhsis__date__month=start_month)

        for record in records:
            count = count + getattr(record, field)

        values[start_month] = float(count)
        start_month = start_month + 1

    return values


# informal settlers
def get_informal_settlers():

    values= {}
    records = InformalSettlers.objects.filter(date__year=datetime.now().year)

    for record in records:
        values[record.date.month] = float(record.families_count)

    return values

# # # # # # # # # # # YEARLY DATA POINTS # # # # # # #


# unemployment rate
def get_unemployment_rate():

    values = {}
    rates = UnemploymentRate.objects.all()

    for rate in rates:
        values[rate.date.year] = float(rate.rate)

    return values


# combine data points to form (x,y) two variables -- MONTHLY
def make_variables(n_status, variable):

    final_list = []

    # sort by key
    sorted_a = sorted(n_status.items())
    sorted_b = sorted(variable.items())

    length = len(sorted_a)

    for x in range(0, length):

        final_list.append(
            (sorted_b[x][1], sorted_a[x][1])
        )

    return final_list


# # # # # # # PEARSON CORRELATION # # # # # #
def get_correlation_score(numbers):

    product = get_sv(numbers, 0) * get_sv(numbers, 1)

    if product == 0:
        return 0

    return round(get_covariance(numbers) / (product ** 0.5), 3)


# get means
def get_means(numbers):

    x = []
    y = []

    for num in numbers:
        x.append(num[0])
        y.append(num[1])

    xbar = numpy.mean(x)
    ybar = numpy.mean(y)

    return xbar, ybar


def get_covariance(numbers):

    xbar = get_means(numbers)[0]
    ybar = get_means(numbers)[1]

    sum = 0
    for number in numbers:
        x = number[0] - xbar
        y = number[1] - ybar

        sum = sum + x * y

    return sum


def get_sv(numbers, n):

    mean = get_means(numbers)[n]

    sum = 0
    for number in numbers:
        sv = (number[n] - mean) ** 2
        sum = sum + sv

    return sum


# # # # # # # # # #

def display(source, scores, model, sex):

    nutritional_statuses = NutritionalStatus.objects.all()

    for status in nutritional_statuses:
        # child care
        for data in source:
            phrase = str(data).split(".")
            field = phrase[2]

            weights = get_weight_values_per_month(status, sex)
            data_point = get_fhsis(model, field, sex)
            score = get_correlation_score(
                make_variables(weights, data_point)
            )

            scores.append(
                {
                    'category': status.name,
                    'sex': sex.name,
                    'source': model.__name__,
                    'field': data.verbose_name,
                    'score': score,
                    'variables': make_variables(weights, data_point)
                }
            )


def display_micronutrient(scores):

    fields = [f for f in ChildCare._meta.get_fields() if f.verbose_name in datapoints.micronutrient]

    for st in w.weights_per_year_to_dict():

        for f in fields:

            point = str(f).strip().split(".")[2]
            data_point = child_care.get_fhsis(ChildCare, point, None)
            score = get_correlation_score(make_variables(st, data_point))

            scores.append(
                {
                    'category': 'Weight for Age - Underweight and Severely Underweight',
                    'source': 'Child Care',
                    'field': f.verbose_name,
                    'score': score,
                    'report': 'Micronutrient Supplementation',
                    'variables': make_variables(st, data_point)
                }
            )

    return scores


def display_maternal(scores):

    fields = [f for f in MaternalCare._meta.get_fields() if f.verbose_name in datapoints.maternal]

    for st in w.weights_per_year_to_dict():

        for f in fields:

            point = str(f).strip().split(".")[2]
            data_point = get_maternal_care(point)
            score = get_correlation_score(make_variables(st, data_point))

            scores.append(
                {
                    'category': 'Weight for Age - Underweight and Severely Underweight',
                    'source': 'Maternal Care',
                    'field': f.verbose_name,
                    'score': score,
                    'report': 'City Maternal Care',
                    'variables': make_variables(st, data_point)
                }
            )

    return scores


def display_child_care(scores):
    fields = [f for f in ChildCare._meta.get_fields() if f.verbose_name in datapoints.child_care]

    for f in fields:
        point = str(f).strip().split(".")[2]
        weights = get_weight_values()
        data_point = get_fhsis(ChildCare, point, None)
        print(data_point)
        score = get_correlation_score(make_variables(weights, data_point))

        scores.append(
            {
                'category': 'Weight for Age - Underweight and Severely Underweight',
                'source': 'Child Care',
                'field': f.verbose_name,
                'score': score,
                'report': 'City Children Care',
                'variables': make_variables(weights, data_point)
            }
        )


def display_no_sex(source, scores, model, sex):

    nutritional_statuses = NutritionalStatus.objects.all()

    for status in nutritional_statuses:
        # child care
        for data in source:
            phrase = str(data).split(".")
            field = phrase[2]

            weights = get_weight_values_per_month(status, sex)
            data_point = get_fhsis_no_sex(model, field)
            score = get_correlation_score(
                make_variables(weights, data_point)
            )

            scores.append(
                {
                    'category': status.name,
                    'sex': sex.name,
                    'source': model.__name__,
                    'field': data.verbose_name,
                    'score': score,
                    'variables': make_variables(weights, data_point)
                }
            )


def display_informal_settlers(scores):

    male = Sex.objects.get(name='Male')
    female = Sex.objects.get(name='Female')

    for status in nutritional_statuses:

        weights = get_weight_values_per_month(status, male)
        score = get_correlation_score(
            make_variables(weights, get_informal_settlers())
        )

        scores.append({
            'category': status.name,
            'sex': male.name,
            'source': 'Informal Settlers',
            'field': 'Number of families',
            'score': score,
            'variables': make_variables(weights, get_informal_settlers())
        })

        weights = get_weight_values_per_month(status, female)
        score = get_correlation_score(
            make_variables(weights, get_informal_settlers())
        )

        scores.append({
            'category': status.name,
            'sex': female.name,
            'source': 'Informal Settlers',
            'field': 'Number of families',
            'score': score,
            'variables': make_variables(weights, get_informal_settlers())
        })


def create_session(request):
    scores = []

    # # # # # # # # # # # # #
    # FEMALE
    # sex = Sex.objects.get(name='Female')
    # sex2 = Sex.objects.get(name='Male')
    #
    # display(
    #     datapoints.get_child_care_fields(),
    #     scores,
    #     ChildCare,
    #     sex
    # )
    #
    # display(
    #     datapoints.get_tb_fields(),
    #     scores,
    #     Tuberculosis,
    #     sex
    # )
    #
    # display(
    #     Malaria._meta.get_fields()[1:6],
    #     scores,
    #     Malaria,
    #     sex
    # )
    #
    # display(
    #     Immunization._meta.get_fields()[1:11],
    #     scores,
    #     Immunization,
    #     sex
    # )
    #
    # display(
    #     Schistosomiasis._meta.get_fields()[1:3],
    #     scores,
    #     Schistosomiasis,
    #     sex
    # )
    #
    # display(
    #     Leprosy._meta.get_fields()[1:3],
    #     scores,
    #     Leprosy,
    #     sex
    # )
    #
    # display(
    #     Flariasis._meta.get_fields()[1:4],
    #     scores,
    #     Flariasis,
    #     sex
    # )
    #
    # display_no_sex(
    #     MaternalCare._meta.get_fields()[1:10],
    #     scores,
    #     MaternalCare,
    #     sex
    # )
    #
    # display_no_sex(
    #     STISurveillance._meta.get_fields()[2:5],
    #     scores,
    #     STISurveillance,
    #     sex
    # )
    #
    # display(
    #     datapoints.get_child_care_fields(),
    #     scores,
    #     ChildCare,
    #     sex2
    # )
    #
    # display(
    #     datapoints.get_tb_fields(),
    #     scores,
    #     Tuberculosis,
    #     sex2
    # )
    #
    # display(
    #     Malaria._meta.get_fields()[1:6],
    #     scores,
    #     Malaria,
    #     sex2
    # )
    #
    # display(
    #     Immunization._meta.get_fields()[1:11],
    #     scores,
    #     Immunization,
    #     sex2
    # )
    #
    # display(
    #     Schistosomiasis._meta.get_fields()[1:3],
    #     scores,
    #     Schistosomiasis,
    #     sex2
    # )
    #
    # display(
    #     Leprosy._meta.get_fields()[1:3],
    #     scores,
    #     Leprosy,
    #     sex2
    # )
    #
    # display(
    #     Flariasis._meta.get_fields()[1:4],
    #     scores,
    #     Flariasis,
    #     sex2
    # )
    #
    # display_no_sex(
    #     MaternalCare._meta.get_fields()[1:10],
    #     scores,
    #     MaternalCare,
    #     sex2
    # )
    #
    # display_no_sex(
    #     STISurveillance._meta.get_fields()[2:5],
    #     scores,
    #     STISurveillance,
    #     sex2
    # )
    #
    # display_informal_settlers(scores)
    display_micronutrient(scores)
    display_maternal(scores)
    display_child_care(scores)

    request.session['scores'] = scores


def get_micronutrient_data():
    pass

