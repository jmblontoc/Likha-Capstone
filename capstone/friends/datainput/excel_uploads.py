import xlrd

from datainput.models import AgeGroup, OPTValues, NutritionalStatus


def upload_eopt(age_group, ns_list, column, opt, sheet):

    counter = 0

    for x in range(5, 18):

        OPTValues.objects.create(
            opt=opt,
            age_group=age_group,
            nutritional_status=NutritionalStatus.objects.get(code=ns_list[counter]),
            values=sheet.cell_value(x, column)
        )

        counter = counter + 1


def is_valid_opt(sheet):

    start = 5
    end = 18

    s = 1
    e = 21

    exceptions = [3, 6, 9, 12, 15, 18, 21]

    for x in range(s, e):
        if x in exceptions:
            continue
        for y in range(start, end):

            cell = sheet.cell_value(y, x)

            if cell == '':
                return False
    return True


def is_valid_fhsis(sheet):

    for a in range(4, 13):
        if sheet.cell_value(a, 1) == '':
            return False

    exceptions = [21, 22, 28, 29, 34, 35, 38, 39, 43, 44, 47, 48]

    for b in range(18, 61):

        if b in exceptions:
            continue

        if sheet.cell_value(b, 1) == '' or sheet.cell_value(b, 2) == '':
            return False

    for c in range(64, 67):
        if sheet.cell_value(c, 1) == '':
            return False

    for d in range(70, 77):
        if sheet.cell_value(d, 1) == '' or sheet.cell_value(d, 2) == '':
            return False

    return True


def return_incomplete_fhsis(sheet):

    rows = []

    for a in range(4, 13):
        print(sheet.cell_value(a, 1))
        if sheet.cell_value(a, 1) == '':
            field = sheet.cell_value(a, 0)

            rows.append({
                'field': field,
                'row': a,
                'column': 1,
                'value': sheet.cell_value(a, 1)
            })

    exceptions = [21, 22, 28, 29, 34, 35, 38, 39, 43, 44, 47, 48]

    for b in range(18, 61):

        if b in exceptions:
            continue

        if sheet.cell_value(b, 1) == '' or sheet.cell_value(b, 2) == '':
            field = sheet.cell_value(b, 0)

            if sheet.cell_value(b, 1) == '':
                rows.append({
                    'field': field,
                    'row': b,
                    'column': 1,
                    'value': sheet.cell_value(b, 1)
                })

            if sheet.cell_value(b, 2) == '':
                rows.append({
                    'field': field,
                    'row': b,
                    'column': 2,
                    'value': sheet.cell_value(b, 2)
                })

    for c in range(64, 67):
        if sheet.cell_value(c, 1) == '':

            field = sheet.cell_value(c, 0)
            rows.append({
                'field': field,
                'row': c,
                'column': 1,
                'value': sheet.cell_value(c, 1)
            })

    for d in range(70, 77):

        if sheet.cell_value(d, 1) == '' or sheet.cell_value(d, 2) == '':

            field = sheet.cell_value(d, 0)

            if sheet.cell_value(d, 1) == '':
                rows.append({
                    'field': field,
                    'row': d,
                    'column': 1,
                    'value': sheet.cell_value(d, 1)
                })

            if sheet.cell_value(d, 2) == '':
                rows.append({
                    'field': field,
                    'row': d,
                    'column': 2,
                    'value': sheet.cell_value(d, 2)
                })

    return rows