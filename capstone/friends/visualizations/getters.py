from datetime import datetime

from django.db.models import Sum

from datainput.models import ChildCare, Immunization, MaternalCare


def get_micronutrient(sex, date_range):

    data = []

    records = ChildCare.objects.filter(fhsis__date__range=date_range, sex=sex)

    data.append(int(records.aggregate(sum=Sum('received_vitamin_A'))['sum']))
    data.append(int(records.aggregate(sum=Sum('received_iron'))['sum']))
    data.append(int(records.aggregate(sum=Sum('received_MNP'))['sum']))
    # data.append(records.aggregate(sum=Sum('diarrhea_with_ORS'))['sum'])
    #
    # immunizations = Immunization.objects.filter(fhsis__date__range=date_range, sex=sex)
    #
    # data.append(immunizations.aggregate(sum=Sum('given_bcg'))['sum'])
    # data.append(immunizations.aggregate(sum=Sum('given_hepa'))['sum'])
    # data.append(immunizations.aggregate(sum=Sum('given_penta'))['sum'])
    # data.append(immunizations.aggregate(sum=Sum('given_opv'))['sum'])
    # data.append(immunizations.aggregate(sum=Sum('given_mcv'))['sum'])
    # data.append(immunizations.aggregate(sum=Sum('given_rota'))['sum'])
    # data.append(immunizations.aggregate(sum=Sum('given_pcv'))['sum'])


    return data


def get_maternal(date_range):

    data = []

    records = MaternalCare.objects.filter(fhsis__date__range=date_range)

    for field in MaternalCare._meta.get_fields()[1:10]:

        phrase = str(field).split(".")
        str_field = phrase[2]

        data.append(
            records.aggregate(sum=Sum(
                str_field
            ))['sum'] or 0
        )

    return data


def get_child_care(date_range):

    data = []

    records = ChildCare.objects.filter(fhsis__date__range=date_range)

    for field in ChildCare._meta.get_fields()[1:13]:
        phrase = str(field).split(".")
        str_field = phrase[2]

        data.append(
            records.aggregate(sum=Sum(
                str_field
            ))['sum'] or 0
        )

    return data