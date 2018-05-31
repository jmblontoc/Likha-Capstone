from datainput.models import Patient, MonthlyReweighing


def has_monthly_reweighing(barangay, month):

    patients = Patient.objects.filter(barangay=barangay)

    for patient in patients:

        try:
            mr = MonthlyReweighing.objects.get(patient=patient, date__month=month)
            print(mr)
        except MonthlyReweighing.DoesNotExist:
            return False

    return True
