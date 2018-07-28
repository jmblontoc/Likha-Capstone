import random
from datetime import datetime
from core.models import Profile
from datainput.models import Barangay, OperationTimbang, NutritionalStatus, AgeGroup, OPTValues, FHSIS, MaternalCare, \
    Immunization, Malaria, Tuberculosis, Schistosomiasis, Flariasis, Leprosy, ChildCare, STISurveillance, FamilyProfile, \
    Sex, FamilyProfileLine


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


def populate_fhsis():

    date = datetime(2015, 3, 5)
    barangays = Barangay.objects.all()

    for barangay in barangays:
        profile = Profile.objects.filter(barangay=barangay).first()

        # create FHSIS
        fhsis = FHSIS(date=date, uploaded_by=profile, barangay=barangay)
        fhsis.save()

        # Maternal Care
        maternal_care = MaternalCare(fhsis=fhsis)

        for field in MaternalCare._meta.get_fields():

            f = str(field).split(".")[2]

            if f == 'fhsis':
                continue

            setattr(maternal_care, f, random.randint(0, 5))

        maternal_care.save()

        # Immunization

        for sex in Sex.objects.all():

            immunization = Immunization(fhsis=fhsis, sex=sex)

            for field in Immunization._meta.get_fields():

                f = str(field).split(".")[2]

                if f == 'fhsis':
                    continue

                if f == 'sex':
                    continue

                setattr(immunization, f, random.randint(0, 5))

            immunization.save()

        # # # #

        for sex in Sex.objects.all():

            malaria = Malaria(fhsis=fhsis, sex=sex)

            for field in Malaria._meta.get_fields():

                f = str(field).split(".")[2]

                if f == 'fhsis':
                    continue

                if f == 'sex':
                    continue

                setattr(malaria, f, random.randint(0, 5))

            malaria.save()

        # # # # #

        for sex in Sex.objects.all():

            tb = Tuberculosis(fhsis=fhsis, sex=sex)

            for field in Tuberculosis._meta.get_fields():

                f = str(field).split(".")[2]

                if f == 'sex':
                    continue

                if f == 'fhsis':
                    continue

                setattr(tb, f, random.randint(0, 5))

            tb.save()

        # # # # #

        for sex in Sex.objects.all():

            schist = Schistosomiasis(fhsis=fhsis, sex=sex)

            for field in Schistosomiasis._meta.get_fields():

                f = str(field).split(".")[2]

                if f == 'sex':
                    continue

                if f == 'fhsis':
                    continue

                setattr(schist, f, random.randint(0, 5))

            schist.save()

        # # # # # # #

        for sex in Sex.objects.all():

            fl = Flariasis(fhsis=fhsis, sex=sex)

            for field in Flariasis._meta.get_fields():

                f = str(field).split(".")[2]

                if f == 'sex':
                    continue

                if f == 'fhsis':
                    continue

                setattr(fl, f, random.randint(0, 5))

            fl.save()

        # # # # # # # #

        for sex in Sex.objects.all():

            lep = Leprosy(fhsis=fhsis, sex=sex)

            for field in Leprosy._meta.get_fields():

                f = str(field).split(".")[2]

                if f == 'sex':
                    continue

                if f == 'fhsis':
                    continue

                setattr(lep, f, random.randint(0, 5))

            lep.save()

        # # # # #

        for sex in Sex.objects.all():

            cc = ChildCare(fhsis=fhsis, sex=sex)

            for field in ChildCare._meta.get_fields():

                f = str(field).split(".")[2]

                if f == 'sex':
                    continue

                if f == 'fhsis':
                    continue

                setattr(cc, f, random.randint(0, 5))

            cc.save()

        # # # #

        sti = STISurveillance(fhsis=fhsis)

        for field in STISurveillance._meta.get_fields():

            f = str(field).split(".")[2]

            if f == 'fhsis':
                continue

            setattr(sti, f, random.randint(0, 5))

        sti.save()

    return "Success"


def populate_family_profile():

    names = ['Pedro', 'Yael', 'Yani', 'Ely', 'Buddy']
    occupations = ['Driver', 'Teacher', 'Doctor', 'Vendor']

    date = datetime(2015, 3, 5)
    barangays = Barangay.objects.all()
    counter = 6727

    for barangay in barangays:

        # Family Profile
        profile = Profile.objects.filter(barangay=barangay).first()
        fp = FamilyProfile(date=date, barangay=barangay, uploaded_by=profile)
        fp.save()

        # create FP Lines

        FamilyProfileLine.objects.create(
            family_profile=fp,
            household_no=counter,
            no_members=random.randint(4, 10),
            count_05=random.randint(2, 5),
            count_623=random.randint(2, 5),
            count_2459=random.randint(2, 5),
            count_60=random.randint(2, 5),
            household_head_name=names[random.randint(0, 4)],
            occupation=occupations[random.randint(0, 3)],
            educational_attainment='Highschool Graduate',
            is_mother_pregnant=True,
            is_family_planning=True,
            is_ebf=True,
            is_mixed_milk_feeding=True,
            is_bottle_feeding=False,
            is_using_iodized_salt=True,
            is_using_ifr=True,
            toilet_type='Water Sealed',
            water_sources='Spring',
            food_production_activity='Fishpond'
        )

        counter -= 22

    return "Success"

