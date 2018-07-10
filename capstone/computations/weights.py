from datetime import datetime

from django.db.models import Sum

from datainput.models import *

month_now = datetime.now().month
year_now = datetime.now().year

# # # # # # IMPORTANT! # # # # # # #
# to get the total weights per time period, Monthly Reweighing must be used, not OPT
# OPT was used here for the demo, but for deployment, Monthly Reweighing must be implemented


def get_weights_per_year_per_status(status, year):

    total = OPTValues.objects.filter(opt__date__year=year, nutritional_status=status).aggregate(
        sum=Sum('values')
    )['sum']

    return float(total)


def weights_per_year_to_dict():

    years = [x.year for x in OperationTimbang.objects.dates('date', 'year')]

    uw = NutritionalStatus.objects.get(code='WU')
    suw = NutritionalStatus.objects.get(code='WSU')

    stunted = NutritionalStatus.objects.get(code='HS')
    severely_stunted = NutritionalStatus.objects.get(code='HSS')

    wasted = NutritionalStatus.objects.get(code='WHW')
    severely_wasted = NutritionalStatus.objects.get(code='WHSW')

    weight_for_age = {}
    height_for_age = {}
    weight_for_height_length = {}

    for year in years:

        weight_for_age[year] = float(get_weights_per_year_per_status(uw, year)
                                     + get_weights_per_year_per_status(suw, year))

        height_for_age[year] = float(get_weights_per_year_per_status(stunted, year)
                                     + get_weights_per_year_per_status(severely_stunted, year))

        weight_for_height_length[year] = float(get_weights_per_year_per_status(wasted, year)
                                     + get_weights_per_year_per_status(severely_wasted, year))

    return [weight_for_age, height_for_age, weight_for_height_length]