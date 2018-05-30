import xlrd

from datainput.models import OPTValues, NutritionalStatus

exceptions = [3, 6, 9, 12, 15, 18, 21]


def upload_eopt(age_group, ns_list, column, opt, sheet):

    counter = 0

    for x in range(5, 18):

        ns = NutritionalStatus.objects.get(code=ns_list[counter])
        OPTValues.objects.create(
            opt=opt,
            age_group=age_group,
            nutritional_status=ns,
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
