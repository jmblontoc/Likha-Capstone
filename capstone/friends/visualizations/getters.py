from datetime import datetime

from django.db.models import Sum

from datainput.models import ChildCare, Immunization


def get_micronutrient(sex):

    data = []

    records = ChildCare.objects.filter(fhsis__date__year=datetime.now().year, sex=sex)

    data.append(records.aggregate(sum=Sum('received_vitamin_A'))['sum'])
    data.append(records.aggregate(sum=Sum('received_iron'))['sum'])
    data.append(records.aggregate(sum=Sum('received_MNP'))['sum'])
    data.append(records.aggregate(sum=Sum('diarrhea_with_ORS'))['sum'])

    immunizations = Immunization.objects.filter(fhsis__date__year=datetime.now().year, sex=sex)

    data.append(immunizations.aggregate(sum=Sum('given_bcg'))['sum'])
    data.append(immunizations.aggregate(sum=Sum('given_hepa'))['sum'])
    data.append(immunizations.aggregate(sum=Sum('given_penta'))['sum'])
    data.append(immunizations.aggregate(sum=Sum('given_opv'))['sum'])
    data.append(immunizations.aggregate(sum=Sum('given_mcv'))['sum'])
    data.append(immunizations.aggregate(sum=Sum('given_rota'))['sum'])
    data.append(immunizations.aggregate(sum=Sum('given_pcv'))['sum'])

    return data

