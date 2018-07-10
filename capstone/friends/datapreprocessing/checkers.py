from datainput.models import Barangay, NutritionalStatus
from datapreprocessing.models import Metric
from friends import datapoints


def has_nutritional():

    metrics = Metric.objects.all()
    statuses = [status.name for status in NutritionalStatus.objects.all()]

    count = 0
    for metric in metrics:
        if metric.get_sex == 'N/A':
            if metric.get_data_point in statuses:
                count = count + 1

    print(count)
    return count == NutritionalStatus.objects.all().count()


def has_micronutrient():

    metrics = Metric.objects.all()
    count = 0

    for metric in metrics:
        if metric.get_sex == 'N/A':
            if metric.get_data_point in datapoints.micronutrient:
                count = count + 1

    return count == 3


def has_maternal():

    metrics = Metric.objects.all()
    count = 0

    for metric in metrics:
        if metric.get_sex == 'N/A':
            if metric.get_data_point in datapoints.maternal:
                count = count + 1

    return count == len(datapoints.maternal)


def has_child_care():

    metrics = Metric.objects.all()
    count = 0

    for metric in metrics:
        if metric.get_sex == 'N/A':
            if metric.get_data_point in datapoints.child_care:
                count = count + 1

    return count == 7


def has_socioeconomic():

    metrics = Metric.objects.all()
    count = 0

    for metric in metrics:
        if metric.get_sex == 'N/A':
            if metric.get_data_point in datapoints.socioeconomic:
                count = count + 1

    return count == datapoints.socioeconomic.__len__()

