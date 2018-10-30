import random
import datetime as d
from datainput.models import *
from friends import revised_datapoints
from friends import datapoints

def populate_opt(year):

    # create an OPT for every barangay
    for barangay in Barangay.objects.all():

        date_create = d.datetime(year, 3, 25, 0, 0, 0, 0)
        opt = OperationTimbang.objects.create(date=date_create, barangay=barangay, uploaded_by=barangay.profile_set.first())

        create_opt_values(opt)

        print(barangay.name)


def create_opt_values(opt):

    for group in AgeGroup.objects.all():
        for status in NutritionalStatus.objects.all():

            random_value = random.randint(0, 2)

            OPTValues.objects.create(
                opt=opt,
                values=random_value,
                nutritional_status=status,
                age_group=group
            )


def delete_opt(year):

    OperationTimbang.objects.filter(date__year=year).delete()
    print('deleted')


def populate_family_profile(year):

    # create a FP instance for every barangay
    for barangay in Barangay.objects.all():

        date_create = d.datetime(year, 3, 25, 0, 0, 0, 0)
        fp = FamilyProfile.objects.create(date=date_create, barangay=barangay,
                                                            uploaded_by=barangay.profile_set.first())

        create_family_profile(fp)

        print('Family Profile data populated for Barangay %s' % barangay.name)


def create_family_profile(profile):

    names = [
        "John Cena",
        "Paul George",
        "George Gervin",
        "Mike Beasley",
        "Alvin Pasaol",
        "Alvin Reyes"
    ]

    occupations = [
        "Driver",
        "Teacher",
        "Engineer",
        "Vendor",
        "Doctor",
        "None",
        "Bank Employee",
        "Waiter",
        "Call Center Agent"
    ]

    FamilyProfileLine.objects.create(
        family_profile=profile,
        household_no=random.randint(100, 5000),
        no_members=random.randint(3, 6),
        count_05=random.randint(0, 3),
        count_623=random.randint(0, 3),
        count_2459=random.randint(0, 3),
        count_60=random.randint(0, 3),
        household_head_name=names[random.randint(0, len(names) - 1)],
        occupation=occupations[random.randint(0, len(occupations) - 1)],
        educational_attainment=datapoints.educational_attainment[random.randint(0, len(datapoints.educational_attainment) - 1)],
        is_mother_pregnant=True,
        is_family_planning=True,
        is_ebf=False,
        is_mixed_milk_feeding=True,
        is_bottle_feeding=False,
        toilet_type=datapoints.toilet_type[random.randint(0, len(datapoints.toilet_type) - 1)],
        water_sources=datapoints.water_sources[random.randint(0, len(datapoints.water_sources) - 1)],
        food_production_activity=datapoints.food_production[random.randint(0, len(datapoints.food_production) - 1)],
        is_using_iodized_salt=True,
        is_using_ifr=False
    )


def populate_fhsis(year):

    for barangay in Barangay.objects.all():

        fhsis = FHSIS.objects.create(
            date=d.datetime(year, 3, 3, 0, 0, 0, 0),
            barangay=barangay,
            uploaded_by=barangay.profile_set.first()
        )

        populate_maternal(fhsis)
        populate_immunization(fhsis)
        populate_malaria(fhsis)
        populate_tb(fhsis)
        populate_sch(fhsis)
        populate_fl(fhsis)
        populate_leprosy(fhsis)
        populate_cc(fhsis)
        populate_sti(fhsis)

def populate_maternal(fhsis):

    fields = MaternalCare._meta.get_fields()[1:12]

    maternal = MaternalCare()
    maternal.fhsis = fhsis

    for f in fields:
        str_field = str(f).split(".")[2]
        random_value = random.randint(0, 60)
        setattr(maternal, str_field, random_value)

    maternal.save()


def populate_sti(fhsis):

    fields = STISurveillance._meta.get_fields()[2:5]

    maternal = STISurveillance()
    maternal.fhsis = fhsis

    for f in fields:
        str_field = str(f).split(".")[2]
        random_value = random.randint(0, 60)
        setattr(maternal, str_field, random_value)

    maternal.save()


def populate_immunization(fhsis):

    fields = Immunization._meta.get_fields()[1:11]

    for sex in Sex.objects.all():

        imm = Immunization()
        imm.sex = sex
        imm.fhsis = fhsis

        for f in fields:
            str_field = str(f).split(".")[2]
            random_value = random.randint(0, 60)
            setattr(imm, str_field, random_value)

        imm.save()


def populate_malaria(fhsis):

    fields = Malaria._meta.get_fields()[1:6]

    for sex in Sex.objects.all():

        imm = Malaria()
        imm.sex = sex
        imm.fhsis = fhsis

        for f in fields:
            str_field = str(f).split(".")[2]
            random_value = random.randint(0, 60)
            setattr(imm, str_field, random_value)

        imm.save()


def populate_tb(fhsis):

    fields = Tuberculosis._meta.get_fields()[1:5]

    for sex in Sex.objects.all():

        imm = Tuberculosis()
        imm.sex = sex
        imm.fhsis = fhsis

        for f in fields:
            str_field = str(f).split(".")[2]
            random_value = random.randint(0, 60)
            setattr(imm, str_field, random_value)

        imm.save()


def populate_sch(fhsis):

    fields = Schistosomiasis._meta.get_fields()[1:3]

    for sex in Sex.objects.all():

        imm = Schistosomiasis()
        imm.sex = sex
        imm.fhsis = fhsis

        for f in fields:
            str_field = str(f).split(".")[2]
            random_value = random.randint(0, 60)
            setattr(imm, str_field, random_value)

        imm.save()


def populate_fl(fhsis):

    fields = Flariasis._meta.get_fields()[1:4]

    for sex in Sex.objects.all():

        imm = Flariasis()
        imm.sex = sex
        imm.fhsis = fhsis

        for f in fields:
            str_field = str(f).split(".")[2]
            random_value = random.randint(0, 60)
            setattr(imm, str_field, random_value)

        imm.save()


def populate_leprosy(fhsis):

    fields = Leprosy._meta.get_fields()[1:3]

    for sex in Sex.objects.all():

        imm = Leprosy()
        imm.sex = sex
        imm.fhsis = fhsis

        for f in fields:
            str_field = str(f).split(".")[2]
            random_value = random.randint(0, 60)
            setattr(imm, str_field, random_value)

        imm.save()


def populate_cc(fhsis):

    fields = ChildCare._meta.get_fields()[1:16]

    for sex in Sex.objects.all():

        imm = ChildCare()
        imm.sex = sex
        imm.fhsis = fhsis

        for f in fields:
            str_field = str(f).split(".")[2]
            random_value = random.randint(0, 60)
            setattr(imm, str_field, random_value)

        imm.save()


# call functions below