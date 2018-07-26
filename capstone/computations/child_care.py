# FHSIS
import operator

from django.db.models import Sum
from django.http import JsonResponse

from computations.weights import year_now, month_now
from friends.datamining import correlations
from datainput.models import *
from friends import  datapoints


# returns child care over the years. was used in correlation
from friends.datapreprocessing.consolidators import get_field


def get_fhsis(model, field, sex):

    start_year = correlations.get_starting_year(FHSIS)

    if sex is None:
        base = model.objects.all()
    else:
        base = model.objects.all()

    values = {

    }

    while start_year < year_now:

        count = 0
        records = base.filter(fhsis__date__year=start_year)

        for record in records:
            try:
                count = count + getattr(record, field)
            except TypeError:
                pass

        values[start_year] = float(count)
        start_year = start_year + 1

    return values


def get_fhsis_average(model, field, sex):
    start_year = correlations.get_starting_year(FHSIS)

    if sex is None:
        base = model.objects.all()
    else:
        base = model.objects.all()

    values = {

    }

    while start_year <= year_now:

        count = 0
        records_count = base.filter(fhsis__date__year=start_year).count()
        records = base.filter(fhsis__date__year=start_year)

        for record in records:
            try:
                count = count + getattr(record, field)
            except TypeError:
                pass

        values[start_year] = float(count / records_count) or 0
        start_year = start_year + 1

    return values


def get_fhsis_average_monthly(model, field):

    start_month = correlations.get_starting_month(FHSIS)
    values = {}
    base = model.objects.all()

    while start_month <= month_now:

        count = 0
        records_count = base.filter(fhsis__date__month=start_month).count()
        records = base.filter(fhsis__date__month=start_month)

        for record in records:
            try:
                count = count + getattr(record, field)
            except TypeError:
                pass

        values[start_month] = round(float(count / records_count), 2) or 0
        start_month = start_month + 1

    return values


def child_care_dashboard():
    cc_fields = datapoints.child_care
    fields = [cc_fields[1], cc_fields[3], cc_fields[5], cc_fields[6]]

    values = []
    for f in fields:
        point = get_field(ChildCare, f).strip()
        value = float(ChildCare.objects.filter(fhsis__date__year=year_now).aggregate(sum=Sum(point))['sum'] or 0)
        values.append(value)

    tb = datapoints.tuberculosis[0]
    malaria = datapoints.malaria[0]

    malaria_point = get_field(Malaria, malaria).strip()
    value = float(Malaria.objects.filter(fhsis__date__year=year_now).aggregate(sum=Sum(malaria_point))['sum'])
    values.append(value)
    fields.append(malaria)

    tb_point = get_field(Tuberculosis, tb).strip()
    value = float(Tuberculosis.objects.filter(fhsis__date__year=year_now).aggregate(sum=Sum(tb_point))['sum'])
    values.append(value)
    fields.append(tb)

    return {
        'fields': fields,
        'values': values
    }

# # # # # MICRONUTRIENT # # # # #


def given_totals():

    data = []
    for vitamin in datapoints.micronutrient:

        field = get_field(ChildCare, vitamin)
        total = ChildCare.objects.filter(fhsis__date__year=year_now).aggregate(sum=Sum(field))['sum']
        data.append(int(total))

    return data


def highest(order):

    main_data = []
    for vitamin in datapoints.micronutrient:
        field = get_field(ChildCare, vitamin)

        data = {}
        for b in Barangay.objects.all():
            total = ChildCare.objects.filter(fhsis__date__year=year_now, fhsis__barangay=b).aggregate(sum=Sum(field))['sum']
            data[b.name] = int(total)

        maximum = max(data, key=data.get)
        minimum = min(data, key=data.get)

        if order == 0:
            main_data.append((maximum, data[maximum]))
        else:
            main_data.append((minimum, data[minimum]))

    return main_data


def micro_per_barangay():

    data = []

    for b in Barangay.objects.all():

        sub_data = [b.name]

        for vitamin in datapoints.micronutrient:
            field = get_field(ChildCare, vitamin)
            total = ChildCare.objects.filter(fhsis__date__year=year_now, fhsis__barangay=b).aggregate(sum=Sum(field))['sum']
            sub_data.append(int(total))

        data.append(sub_data)

    return data


def top3_barangays(order):

    barangays = Barangay.objects.all()

    data = []

    for b in barangays:

        sub_data = {'barangay': b.name}
        values = {}
        total_vitamin = 0
        for vitamin in datapoints.micronutrient:
            field = get_field(ChildCare, vitamin)
            sub_total = ChildCare.objects.filter(fhsis__date__year=year_now, fhsis__barangay=b).aggregate(
                sum=Sum(field)
            )['sum']

            values[vitamin] = int(sub_total)
            total_vitamin += int(sub_total)
            sub_data['values'] = values
            sub_data['total'] = total_vitamin

        data.append(sub_data)

    if order == 0:
        new_list = sorted(data, key=operator.itemgetter('total'))[:3]

    else:
        new_list = sorted(data, key=operator.itemgetter('total'), reverse=True)[:3]

    bars = [b['barangay'] for b in new_list]
    vit_a = [b['values'][list(b['values'].keys())[0]] for b in new_list]
    iron = [b['values'][list(b['values'].keys())[1]] for b in new_list]
    mnp = [b['values'][list(b['values'].keys())[2]] for b in new_list]

    return {
        'barangays': bars,
        'vitaminA': vit_a,
        'iron': iron,
        'mnp': mnp
    }


# # # # # REPORT MICRO # # # # # 

def report_table_micro():

    existing_table = micro_per_barangay()

    for data in existing_table:
        total = sum(data[1:])
        data.append(total)

    return existing_table

