import random
from datetime import datetime
from core.models import Profile
from datainput.models import Barangay, OperationTimbang, NutritionalStatus, AgeGroup, OPTValues


def month_converter(month):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return months[month - 1]


def populate_opt():

    date = datetime(2015, 3, 5)
    barangays = Barangay.objects.all()

    for barangay in barangays:

        # create OPT
        profile = Profile.objects.filter(barangay=barangay).first()
        opt = OperationTimbang(date=date, barangay=barangay, uploaded_by=profile)
        opt.save()

        # create OPT Values

        for x in NutritionalStatus.objects.all():
            for y in AgeGroup.objects.all():

                OPTValues.objects.create(
                    opt=opt,
                    nutritional_status=x,
                    age_group=y,
                    values=random.randint(0, 4)
                )

    return "Success"

