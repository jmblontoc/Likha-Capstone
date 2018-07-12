from django.db.models import Sum

from computations.weights import year_now
from friends import datapoints
from computations import weights
from datainput.models import FamilyProfileLine

fields = [
    'Is Practicing Family Planning',
    'Is Practicing Exclusive Breastfeeding',
    'Is Practicing Mixed Milk Feeding',
    'Is Practicing Bottled Feeding',
    'Is Using Iodized Salt',
    'Is Using Iron Fortification',
]

number_of_members = [
    'Total Members'
]

def get_socioeconomic(field):

    start_year = FamilyProfileLine.objects.dates('family_profile__date', 'year')[0].year
    year_now = weights.year_now

    values = {}

    f = get_field_via_verbose(field)

    while start_year <= year_now:

        records = FamilyProfileLine.objects.filter(family_profile__date__year=start_year)

        count = 0
        for r in records:
            if getattr(r, f):
                count = count + 1

        values[start_year] = count
        start_year = start_year + 1

    return values


def get_field_via_verbose(field):

    for f in FamilyProfileLine._meta.get_fields():
        if f.verbose_name == field:
            return str(f).strip().split(".")[2]


def get_members_data():
    start_year = FamilyProfileLine.objects.dates('family_profile__date', 'year')[0].year
    year_now = weights.year_now

    values = {}

    while start_year <= year_now:

        records = FamilyProfileLine.objects.filter(
            family_profile__date__year=start_year).aggregate(sum=Sum('no_members'))['sum']

        values[start_year] = float(records)
        start_year = start_year + 1

    return values


def get_educational_attainment(education):

    start_year = FamilyProfileLine.objects.dates('family_profile__date', 'year')[0].year
    year_now = weights.year_now

    values = {}


    while start_year <= year_now:

        records = FamilyProfileLine.objects.filter(
            family_profile__date__year=start_year,
            educational_attainment=education).count()

        values[start_year] = float(records)
        start_year = start_year + 1

    return values


def get_toilet_type(toilet):

    start_year = FamilyProfileLine.objects.dates('family_profile__date', 'year')[0].year
    year_now = weights.year_now

    values = {}

    while start_year <= year_now:
        records = FamilyProfileLine.objects.filter(
            family_profile__date__year=start_year,
            toilet_type=toilet).count()

        values[start_year] = float(records)
        start_year = start_year + 1

    return values


def get_food_production(way):
    start_year = FamilyProfileLine.objects.dates('family_profile__date', 'year')[0].year
    year_now = weights.year_now

    values = {}

    while start_year <= year_now:
        records = FamilyProfileLine.objects.filter(
            family_profile__date__year=start_year,
            food_production_activity=way).count()

        values[start_year] = float(records)
        start_year = start_year + 1

    return values


def get_water_source(source):
    start_year = FamilyProfileLine.objects.dates('family_profile__date', 'year')[0].year
    year_now = weights.year_now

    values = {}

    while start_year <= year_now:
        records = FamilyProfileLine.objects.filter(
            family_profile__date__year=start_year,
            water_sources=source).count()

        values[start_year] = float(records)
        start_year = start_year + 1

    return values


def get_breastfeeding():

    records = FamilyProfileLine.objects.filter(family_profile__date__year=year_now)
    total = float(records.count())

    ebf = float(records.filter(is_ebf=True).count()) / total
    ebf = round(ebf, 2) * 100

    return [
        {'name': 'Exclusive Breastfeeding', 'y': ebf, 'sliced': 'true'},
        {'name': 'Bottled Feeding', 'y': 100 - ebf}
    ]









