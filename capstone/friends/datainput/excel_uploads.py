import datetime
import os
import xlrd

from capstone import settings
from datainput.models import AgeGroup, OPTValues, NutritionalStatus, Sex, Patient


def upload_patient_data(sheet, book, barangay):

    x = 6
    while True:

        try:

            name = sheet.cell_value(x, 3)
            sex = sheet.cell_value(x, 5)
            birth = sheet.cell_value(x, 6)

            dt = datetime.datetime(*xlrd.xldate_as_tuple(birth, book.datemode))

            if birth == 'M':
                sex = Sex.objects.get(name='Male')
            else:
                sex = Sex.objects.get(name='Female')

            Patient.objects.create(
                name=name,
                sex=sex,
                date_of_birth=dt,
                barangay=barangay
            )

            x += 1
        except IndexError:
            break


def dummy():

    temp_path = os.path.join(settings.MEDIA_ROOT, 'eopt')
    renamed = os.path.join(temp_path, "34.xlsx")

    workbook = xlrd.open_workbook(renamed)
    sheet = workbook.sheet_by_index(2)

    return sheet.cell(19, 2)


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