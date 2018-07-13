from datetime import datetime

from django.db.models import Sum

from datainput.models import *
from computations.weights import month_now, year_now
from datainput.models import MaternalCare
from friends import datapoints
from friends.datamining import correlations as c


# returns maternal over the years. was used in correlation
from friends.datapreprocessing.consolidators import get_field


def get_maternal_care(field):

    start_year = c.get_starting_year(FHSIS)
    base = MaternalCare.objects.all()

    values = {

    }

    while start_year <= year_now:

        count = 0
        records = base.filter(fhsis__date__year=start_year)

        for record in records:
            count = count + getattr(record, field)

        values[start_year] = int(count)
        start_year = start_year + 1

    return values


def maternal_dashboard(view):
    maternal_fields = datapoints.maternal
    fields = [maternal_fields[0], maternal_fields[2]]

    # for view
    if view is not None:
        values = []
        for f in fields:
            point = get_field(MaternalCare, f).strip()
            value = float(MaternalCare.objects.filter(fhsis__date__year=year_now).aggregate(sum=Sum(point))['sum'] or 0)

            values.append({
                f: value
            })

        return values

    values = []
    for f in fields:
        point = get_field(MaternalCare, f).strip()
        value = float(MaternalCare.objects.filter(fhsis__date__year=year_now).aggregate(sum=Sum(point))['sum'] or 0)
        values.append(value)

    return {
        'fields': fields,
        'values': values
    }
