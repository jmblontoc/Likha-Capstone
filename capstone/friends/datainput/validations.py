from datetime import datetime

from datainput.models import Patient, MonthlyReweighing, HealthCareWasteManagement, InformalSettlers, UnemploymentRate


def has_monthly_reweighing(barangay, month):

    patients = Patient.objects.filter(barangay=barangay)

    for patient in patients:

        try:
            mr = MonthlyReweighing.objects.get(patient=patient, date__month=month)
            print(mr)
        except MonthlyReweighing.DoesNotExist:
            return False

    return True


def is_updated(patient):

    reweighs = MonthlyReweighing.objects.filter(patient=patient)

    if reweighs.count() == 0:
        return False

    for weighs in reweighs:

        if weighs.date.month == datetime.now().month and weighs.date.year == datetime.now().year:
            return True

    return False


def has_health_care():

    record = HealthCareWasteManagement.objects.filter(
        date__year=datetime.now().year
    )

    return record.count() > 0


def has_informal_settlers():

    return InformalSettlers.objects.filter(date__year=datetime.now().year).count() > 0


def has_unemployment_rate():

    return UnemploymentRate.objects.filter(date__year=datetime.now().year).count() > 0
