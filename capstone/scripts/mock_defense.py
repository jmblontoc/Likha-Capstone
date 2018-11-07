from causalmodel.models import  *
from datapreprocessing.models import *
from datainput.models import *

RootCause.objects.filter(date__year=2018).delete()
CausalModel.objects.filter(date__year=2018).delete()


# thresholds
Metric.objects.filter(metric__contains='Given BCG', date__year=2018).delete()
Metric.objects.filter(metric__contains='Anemic c', date__year=2018).delete()
Metric.objects.filter(metric__contains='Malaria C', date__year=2018).delete()

# BNS
FHSIS.objects.filter(date__year=2018, date__month=11, barangay__name__contains='Ibaba').delete()
OperationTimbang.objects.filter(date__year=2018, barangay__name__contains='Ibaba').delete()
FamilyProfile.objects.filter(date__year=2018, barangay__name__contains='Ibaba').delete()
MonthlyReweighing.objects.filter(date__year=2018, date__month=11, patient__barangay__name__contains='Ibaba').delete()
Patient.objects.filter(barangay__name__contains='Ibaba').delete()