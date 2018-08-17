from django.db.models import Sum
from django.http import JsonResponse

from computations.weights import year_now
from friends import revised_datapoints, datapoints
from computations.child_care import get_fhsis
from datainput.models import Tuberculosis, Malaria, ChildCare, MaternalCare, FamilyProfile, FamilyProfileLine, \
    Immunization, InformalSettlers

# get total values per year over time with forecast
# all are FHSIS
from friends.datapreprocessing.consolidators import get_field


def get_value(field):

    if field not in revised_datapoints.SOCIOECONOMIC:

        # filter the fields
        if field == 'Number of Tuberculosis Identified':
            model = Tuberculosis

        elif field == 'Number of Malaria Cases':
            model = Malaria

        elif field in revised_datapoints.MATERNAL:
            model = MaternalCare

        elif field in datapoints.immunizations:
            model = Immunization

        elif field in revised_datapoints.INFORMAL:
            model = InformalSettlers

            # compute informal settlers
            a = InformalSettlers.objects.dates('date', 'year')
            year_start = a[0].year

            values = {}
            while year_start < year_now:
                total = InformalSettlers.objects.filter(date__year=year_start).aggregate(
                    sum=Sum('families_count'))['sum']
                values[year_start] = int(total)

                year_start += 1

            return values, model.__name__

        else:
            model = ChildCare

        model_field = get_field(model, field)

        return get_fhsis(model, model_field, None), model.__name__

    else:

        # SOCIOECONOMIC
        years = FamilyProfile.objects.dates('date', 'year')
        start_year = sorted(years)[0].year
        query = FamilyProfileLine.objects.all()

        if field == revised_datapoints.SOCIOECONOMIC[0]:  # water source well

            values = {}

            while start_year < year_now:

                total = query.filter(family_profile__date__year=start_year).filter(
                    water_sources__contains='Well'
                ).count()

                values[start_year] = int(total)

                start_year += 1

            # return values

        elif field == revised_datapoints.SOCIOECONOMIC[1]:  # open pit

            values = {}

            while start_year < year_now:
                total = query.filter(family_profile__date__year=start_year).filter(
                    toilet_type__contains='Open Pit'
                ).count()

                values[start_year] = int(total)

                start_year += 1

            # return values

        elif field == revised_datapoints.SOCIOECONOMIC[2]:  # no toilet

            values = {}

            while start_year < year_now:
                total = query.filter(family_profile__date__year=start_year).filter(
                    toilet_type__contains='None'
                ).count()

                values[start_year] = int(total)

                start_year += 1

            # return values

        elif field == revised_datapoints.SOCIOECONOMIC[3]:  # undergraduate parents

            values = {}

            while start_year < year_now:
                total = query.filter(family_profile__date__year=start_year).filter(
                    educational_attainment__contains='Elementary Undergraduate'
                ).count()

                values[start_year] = int(total)

                start_year += 1

            # return values

        elif field == revised_datapoints.SOCIOECONOMIC[4]:  # practicing family planning

            values = {}

            while start_year < year_now:
                total = query.filter(family_profile__date__year=start_year).filter(
                    is_family_planning=True
                ).count()

                values[start_year] = int(total)

                start_year += 1

            # return values

        elif field == revised_datapoints.SOCIOECONOMIC[5]:  # iodized salt

            values = {}

            while start_year < year_now:
                total = query.filter(family_profile__date__year=start_year).filter(
                    is_using_iodized_salt=True
                ).count()

                values[start_year] = int(total)

                start_year += 1

            # return values

        return values, 'Family Profile'

