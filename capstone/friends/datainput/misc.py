import datetime
from datetime import datetime as dt


def get_fields(model):

    fields = model._meta.get_fields()

    result = []

    for field in fields:

        phrase = str(field).split('.')
        result.append(phrase[2])

    return result


def get_due_date(time):

    if time == 'monthly':

        month = dt.now().month
        year = dt.now().year

        if month == 2:
            day = 28

        day = 30

        return datetime.date(year, month, day)

    else:

        month = 3
        year = dt.now().year

        return datetime.date(year, month, 30)