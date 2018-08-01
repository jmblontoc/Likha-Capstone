import json
import random
import string

from django.apps import apps
from django.db.models import Sum

from computations.weights import year_now
from friends import revised_datapoints, datapoints
from datainput.models import *
from computations import weights
from friends.datapreprocessing import consolidators
from friends.datapreprocessing.consolidators import get_field


def get_source(field):

    print(field)

    if field in revised_datapoints.ILLNESSES[0:6]:
        return "Child Care"
    if field in revised_datapoints.ILLNESSES[6:7]:
        return "Tuberculosis"
    if field in revised_datapoints.ILLNESSES[7:8]:
        return "Malaria"
    if field in revised_datapoints.MATERNAL:
        return "Maternal Care"
    if field in revised_datapoints.SOCIOECONOMIC:
        return "Family Profile"
    if field in datapoints.micronutrient:
        return "Child Care"
    if field in datapoints.immunizations:
        return "Immunization"

    return None


def get_value_until_present(source, field):

    point = field

    # hard coded
    if point == revised_datapoints.SOCIOECONOMIC[0]: point = 'Well'
    elif point == revised_datapoints.SOCIOECONOMIC[1]: point = 'Open Pit'
    elif point == revised_datapoints.SOCIOECONOMIC[2]: point = 'None'
    elif point == revised_datapoints.SOCIOECONOMIC[3]: point = 'Elementary Undergraduate'
    elif point == revised_datapoints.SOCIOECONOMIC[4]: point = 'Number of families practicing family planning'
    elif point == revised_datapoints.SOCIOECONOMIC[5]: point = 'Number of families using iodized salt'

    if source == 'Family Profile':

        if point in datapoints.water_sources:
            start_year = [d.year for d in FamilyProfileLine.objects.dates('family_profile__date', 'year')][0]

            data = {}
            while start_year <= weights.year_now:

                count = FamilyProfileLine.objects.filter(family_profile__date__year=start_year, water_sources=point).count()

                data[start_year] = count
                start_year = start_year + 1

            return json.dumps(data)

        if point in datapoints.food_production:
            start_year = [d.year for d in FamilyProfileLine.objects.dates('family_profile__date', 'year')][0]

            data = {}
            while start_year <= weights.year_now:

                count = FamilyProfileLine.objects.filter(family_profile__date__year=start_year, food_production_activity=point).count()

                data[start_year] = count
                start_year = start_year + 1

            return json.dumps(data)

        if point in datapoints.educational_attainment_for_r:
            start_year = [d.year for d in FamilyProfileLine.objects.dates('family_profile__date', 'year')][0]

            data = {}
            while start_year <= weights.year_now:

                count = FamilyProfileLine.objects.filter(family_profile__date__year=start_year, educational_attainment=point).count()

                data[start_year] = count
                start_year = start_year + 1

            return json.dumps(data)

        if point in datapoints.toilet_type:
            start_year = [d.year for d in FamilyProfileLine.objects.dates('family_profile__date', 'year')][0]

            data = {}
            while start_year <= weights.year_now:

                count = FamilyProfileLine.objects.filter(family_profile__date__year=start_year, toilet_type=point).count()

                data[start_year] = count
                start_year = start_year + 1

            return json.dumps(data)

        field = consolidators.get_field(FamilyProfileLine, point)
        start_year = [d.year for d in FamilyProfileLine.objects.dates('family_profile__date', 'year')][0]

        data = {}
        while start_year <= weights.year_now:

            count = 0
            for f in FamilyProfileLine.objects.filter(family_profile__date__year=start_year):
                if getattr(f, field):
                    count = count + 1

            data[start_year] = count
            start_year = start_year + 1

        return json.dumps(data)

    elif source == 'Maternal Care':

        field = consolidators.get_field(MaternalCare, point)
        start_year = [d.year for d in MaternalCare.objects.all().dates('fhsis__date', 'year')][0]

        data = {}
        while start_year <= weights.year_now:
            data[start_year] = float(MaternalCare.objects.filter(fhsis__date__year=start_year).aggregate(sum=Sum(field))['sum'])
            start_year += 1

        return json.dumps(data)

    elif source == 'Child Care':

        field = consolidators.get_field(ChildCare, point)
        start_year = [d.year for d in
                       ChildCare.objects.all().dates('fhsis__date', 'year')][0]

        data = {}
        while start_year <= weights.year_now:
            data[start_year] = float(ChildCare.objects.filter(fhsis__date__year=start_year).aggregate(
                sum=Sum(field))['sum'])
            start_year += 1

        return json.dumps(data)

    elif source == 'Malaria':

        field = consolidators.get_field(Malaria, point)
        start_year = [d.year for d in
                       Malaria.objects.all().dates('fhsis__date', 'year')][0]

        data = {}
        while start_year <= weights.year_now:
            data[start_year] = float(Malaria.objects.filter(fhsis__date__year=start_year).aggregate(
                sum=Sum(field))['sum'])
            start_year += 1

        return json.dumps(data)

    elif source == 'Immunization':

        field = consolidators.get_field(Immunization, point)
        start_year = [d.year for d in
                       Immunization.objects.all().dates('fhsis__date', 'year')][0]

        data = {}
        while start_year <= weights.year_now:
            data[start_year] = float(Immunization.objects.filter(fhsis__date__year=start_year).aggregate(
                sum=Sum(field))['sum'])
            start_year += 1

        return json.dumps(data)

    elif source == 'Tuberculosis':

        field = consolidators.get_field(Tuberculosis, point)
        start_year = [d.year for d in
                       Tuberculosis.objects.all().dates('fhsis__date', 'year')][0]

        data = {}
        while start_year <= weights.year_now:
            data[start_year] = float(Tuberculosis.objects.filter(fhsis__date__year=start_year).aggregate(
                sum=Sum(field))['sum'])
            start_year += 1

        return json.dumps(data)

    return "Wow"


def get_distribution_per_barangay(source, data_point):



    if source == 'Family Profile':
        query = FamilyProfileLine.objects.filter(family_profile__date__year=year_now)

        if data_point == 'Number of families using a Well as water source':

            data = []
            for barangay in Barangay.objects.all():
                total = query.filter(family_profile__barangay=barangay).filter(water_sources='Well').count()
                data.append([barangay.name, int(total)])

            return data

        if data_point == 'Number of families using an Open Pit toilet type':

            data = []
            for barangay in Barangay.objects.all():
                total = query.filter(family_profile__barangay=barangay).filter(toilet_type='Open Pit').count()
                data.append([barangay.name, int(total)])

            return data

        if data_point == 'Number of families who do not have toilets':

            data = []
            for barangay in Barangay.objects.all():
                total = query.filter(family_profile__barangay=barangay).filter(toilet_type='None').count()
                data.append([barangay.name, int(total)])

            return data

        if data_point == 'Number of Elementary Undergraduate Parents':

            data = []
            for barangay in Barangay.objects.all():
                total = query.filter(family_profile__barangay=barangay).filter(
                    educational_attainment='Elementary Undergraduate').count()
                data.append([barangay.name, int(total)])

            return data

        if data_point == 'Number of families using iodized salt':

            data = []
            for barangay in Barangay.objects.all():
                total = query.filter(family_profile__barangay=barangay).filter(is_using_iodized_salt=True).count()
                data.append([barangay.name, int(total)])

            return data

        if data_point == 'Number of families practicing Family Planning':

            data = []
            for barangay in Barangay.objects.all():
                total = query.filter(family_profile__barangay=barangay).filter(is_family_planning=True).count()
                data.append([barangay.name, int(total)])

            return data

    trimmed = source.replace(' ', '')

    model = apps.get_model('datainput', trimmed)

    field = get_field(model, data_point)
    query = model.objects.all().filter(fhsis__date__year=year_now)

    data = []
    for barangay in Barangay.objects.all():
        total = query.filter(fhsis__barangay=barangay).aggregate(sum=Sum(field))['sum']
        data.append([barangay.name, int(total)])

    return data


def to_high_charts(my_dict):

    print(my_dict, type(my_dict))

    values = eval(my_dict)
    years = sorted([key for key, value in values.items()])
    data = [value for key, value in values.items()]

    return [years, data]


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
