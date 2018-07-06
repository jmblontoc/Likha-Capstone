from datetime import datetime

from datainput.models import Patient, MonthlyReweighing, HealthCareWasteManagement, InformalSettlers, UnemploymentRate, \
    FHSIS, OperationTimbang, FamilyProfile, Barangay


def has_monthly_reweighing(barangay, month, year):

    patients = Patient.objects.filter(barangay=barangay)

    if patients.count() == 0:
        return False

    for patient in patients:

        try:
            mr = MonthlyReweighing.objects.get(patient=patient, date__month=month, date__year=year)
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

    return InformalSettlers.objects.filter(date__year=datetime.now().year, date__month=datetime.now().month).count() > 0


def has_unemployment_rate():

    return UnemploymentRate.objects.filter(date__year=datetime.now().year).count() > 0


# # # # # # # # # # # # # # # # # # # # # # # # # #

def todo_list():

    barangays = Barangay.objects.all()

    todo = []

    for b in barangays:

        if not b.has_opt:
            todo.append({
                'report_name': 'Operation Timbang',
                'barangay': b.name
            })

        if not b.has_family_profile:
            todo.append({
                'report_name': 'Family Profile',
                'barangay': b.name
            })

        if not b.has_reweighed:
            todo.append({
                'report_name': 'Monthly Reweighing',
                'barangay': b.name
            })

        if not b.has_fhsis:
            todo.append({
                'report_name': 'FHSIS',
                'barangay': b.name
            })

    return todo

