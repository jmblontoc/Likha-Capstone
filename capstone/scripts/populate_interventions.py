import json

import xlrd
from capstone import settings
from causalmodel.models import SuggestedIntervention
from computations.weights import year_now
from datapreprocessing.models import Metric

path = 'C:\\Users\jmlon\Documents\metrics-revised.xlsx'


def populate():

    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_index(2)

    for x in range(0, 34):

        metric_excel = sheet.cell_value(0, x)
        metric = Metric.objects.get(metric__contains=metric_excel)
        metric.suggested_interventions = ''

        interventions = []
        intervention = sheet.cell_value(1, x)
        interventions.append(intervention)

        metric.suggested_interventions = json.dumps(interventions)
        metric.save()


def populate_revised():

    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_index(2)

    for x in range(0, 34):
        metric = Metric.objects.get(metric__contains=sheet.cell_value(0, x), date__year=year_now)
        name = sheet.cell_value(1, x)
        reason = sheet.cell_value(2, x)

        SuggestedIntervention.objects.create(
            name=name,
            reason=reason,
            metric=metric
        )

# # # # #

populate_revised()