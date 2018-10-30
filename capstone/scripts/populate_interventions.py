import json

import xlrd
from capstone import settings
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


# # # # #


populate()