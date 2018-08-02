from django.db.models import Sum, Avg, Max

from computations.weights import year_now
from friends import datapoints
from computations import weights
from datainput.models import FamilyProfileLine, Barangay, FamilyProfile

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

    while start_year < year_now:

        records = FamilyProfileLine.objects.filter(family_profile__date__year=start_year)

        count = 0
        for r in records:
            if getattr(r, f):
                count = count + 1

        values[start_year] = count
        start_year = start_year + 1

    return values


def get_socioeconomic_average(field):

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

        values[start_year] = count / records.count()
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

    while start_year < year_now:

        records = FamilyProfileLine.objects.filter(
            family_profile__date__year=start_year).aggregate(sum=Sum('no_members'))['sum']

        values[start_year] = float(records)
        start_year = start_year + 1

    return values


def get_members_data_average():
    start_year = FamilyProfileLine.objects.dates('family_profile__date', 'year')[0].year
    year_now = weights.year_now

    values = {}

    while start_year <= year_now:

        records = FamilyProfileLine.objects.filter(
            family_profile__date__year=start_year).aggregate(sum=Sum('no_members'))['sum']

        values[start_year] = float(records/ FamilyProfileLine.objects.filter(family_profile__date__year=start_year).count())
        start_year = start_year + 1

    return values


def get_educational_attainment(education):

    start_year = FamilyProfileLine.objects.dates('family_profile__date', 'year')[0].year
    year_now = weights.year_now

    values = {}


    while start_year < year_now:

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

    while start_year < year_now:
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

    while start_year < year_now:
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

    while start_year < year_now:
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


def report_table():

    data = []
    barangays = Barangay.objects.all().order_by('name')

    for b in barangays:

        query = FamilyProfileLine.objects.filter(family_profile__date__year=year_now, family_profile__barangay=b)
        sub_data = [b.name]

        average_size = query.aggregate(avg=Avg('no_members'))['avg']
        sub_data.append(round(average_size))

        sub_data.append(
            query.aggregate(max=Max('educational_attainment'))['max']
        )

        sub_data.append(
            query.aggregate(max=Max('occupation'))['max']
        )

        sub_data.append(
            query.aggregate(max=Max('water_sources'))['max']
        )

        sub_data.append(
            query.aggregate(max=Max('food_production_activity'))['max']
        )

        sub_data.append(
            query.aggregate(max=Max('toilet_type'))['max']
        )

        sub_data.append(
            query.filter(toilet_type='Water Sealed').count() / query.count()
        )

        data.append(sub_data)

    return data

def report_table_per_year(year):

    data = []
    barangays = Barangay.objects.all().order_by('name')

    for b in barangays:

        query = FamilyProfileLine.objects.filter(family_profile__date__year=year, family_profile__barangay=b)
        sub_data = [b.name]

        average_size = query.aggregate(avg=Avg('no_members'))['avg']
        sub_data.append(round(average_size))

        sub_data.append(
            query.aggregate(max=Max('educational_attainment'))['max']
        )

        sub_data.append(
            query.aggregate(max=Max('occupation'))['max']
        )

        sub_data.append(
            query.aggregate(max=Max('water_sources'))['max']
        )

        sub_data.append(
            query.aggregate(max=Max('food_production_activity'))['max']
        )

        sub_data.append(
            query.aggregate(max=Max('toilet_type'))['max']
        )

        sub_data.append(
            query.filter(toilet_type='Water Sealed').count() / query.count()
        )

        data.append(sub_data)

    return data

def report_table_sort_year():

    data = []
    query = FamilyProfile.objects.dates("date", "year")

    for q in query:
        data.append(q.year)

    return data










