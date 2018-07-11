# FHSIS
from django.db.models import Sum

from computations.weights import year_now
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

    while start_year <= year_now:

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


def child_care_dashboard():
    cc_fields = datapoints.child_care
    fields = [cc_fields[1], cc_fields[3], cc_fields[5], cc_fields[6]]

    values = []
    for f in fields:
        point = get_field(ChildCare, f).strip()
        value = float(ChildCare.objects.filter(fhsis__date__year=year_now).aggregate(sum=Sum(point))['sum'])
        values.append(value)

    return {
        'fields': fields,
        'values': values
    }