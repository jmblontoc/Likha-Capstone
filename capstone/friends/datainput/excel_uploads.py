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

    c = 0

    for x in range(s, e):
        if x in exceptions:
            continue

        for y in range(start, end):

            cell = int(sheet.cell_value(y, x))

            print(type(cell))

    return True
