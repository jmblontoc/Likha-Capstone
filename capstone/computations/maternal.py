from datetime import datetime
from datainput.models import *
from computations.weights import month_now, year_now
from datainput.models import MaternalCare
from friends.datamining import correlations as c


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