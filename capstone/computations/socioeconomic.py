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

def get_socioeconomic(field):

    records = FamilyProfileLine.objects.all()
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



