# FHSIS
from computations.weights import year_now
from friends.datamining import correlations
from datainput.models import *


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