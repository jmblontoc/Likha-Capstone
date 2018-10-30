from causalmodel.models import *
from datainput.models import *

RootCause.objects.filter(date__year=2018).delete()
CausalModel.objects.filter(date__year=2018).delete()

# FHSIS.objects.filter(date__year=2018, date__month=10, barangay=Barangay.objects.first()).delete()