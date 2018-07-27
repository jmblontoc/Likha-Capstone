import decimal
import operator
from datetime import datetime
from random import random

from django.db.models import Sum, Q

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

    return float(total or 0)


def weights_per_year_to_dict():

    years = [x.year for x in OperationTimbang.objects.dates('date', 'year')][:-1]

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


def get_totals_per_year():

    data = {}

    for status in NutritionalStatus.objects.all():

        data[status.name] = float(OPTValues.objects.filter(opt__date__year=year_now, nutritional_status=status).aggregate(
            sum=Sum('values')
        )['sum'])

    return data


# # # # # # # for nutritionist dashboard # # # # # #

def get_computations_per_category(category):

    fields = [status for status in NutritionalStatus.objects.all() if category == status.name.split("-")[0].strip()]
    total = sum([get_weights_per_year_per_status(status, year_now) for status in fields]) or 1

    data = []
    for f in fields:
        sub_data = []
        sub_total = get_weights_per_year_per_status(f, year_now)
        prevalence_rate = round(sub_total / total, 4) * 100
        prevalence_rate = format(prevalence_rate, '.2f')

        # tinanggal na yung mga weight for age ek ek
        normalize = f.name.strip().split(" ")[4:]

        foo = ''
        for a in normalize:
            foo += ' %s' % a
        # # # # # #

        sub_data.append(foo)
        sub_data.append(sub_total)
        sub_data.append(str(prevalence_rate) + '%')
        data.append(sub_data)

    return {
        'data': data,
        'total': total
    }


# # # # # # # # for insights # # # # # # # # # #

# totals
def totals_per_category():

    # SUW and UW
    uw = NutritionalStatus.objects.get(name__contains='Weight for Age - Underweight')
    suw = NutritionalStatus.objects.get(name__contains='Weight for Age - Severely Underweight')
    first = OPTValues.objects.filter(Q(nutritional_status=uw) | Q(nutritional_status=suw)).filter(opt__date__year=year_now).aggregate(sum=Sum('values'))['sum']

    # S and SS
    uw = NutritionalStatus.objects.get(name__contains='Height for Age - Stunted')
    suw = NutritionalStatus.objects.get(name__contains='Height for Age - Severely Stunted')
    second = OPTValues.objects.filter(Q(nutritional_status=uw) | Q(nutritional_status=suw)).filter(
        opt__date__year=year_now).aggregate(sum=Sum('values'))['sum']

    # W and SW
    uw = NutritionalStatus.objects.get(name__contains='Weight for Height/Length - Wasted')
    suw = NutritionalStatus.objects.get(name__contains='Weight for Height/Length - Severely Wasted')
    third = OPTValues.objects.filter(Q(nutritional_status=uw) | Q(nutritional_status=suw)).filter(
        opt__date__year=year_now).aggregate(sum=Sum('values'))['sum']

    return [int(first), int(second), int(third)]


# barangay - highest per category
def highest_barangay_per_category():

    barangays = Barangay.objects.all()

    uw = NutritionalStatus.objects.get(name__contains='Weight for Age - Underweight')
    suw = NutritionalStatus.objects.get(name__contains='Weight for Age - Severely Underweight')

    tops = []
    data = {}

    for b in barangays:
        total = OPTValues.objects.filter(Q(nutritional_status=uw) | Q(nutritional_status=suw)).filter(
        opt__date__year=year_now).filter(opt__barangay=b).aggregate(sum=Sum('values'))['sum']
        data[b.name] = int(total)

    a = max(data.items(), key=operator.itemgetter(1))[0]
    tops.append(a)

    # S and SS
    uw = NutritionalStatus.objects.get(name__contains='Height for Age - Stunted')
    suw = NutritionalStatus.objects.get(name__contains='Height for Age - Severely Stunted')

    data = {}

    for b in barangays:
        total = OPTValues.objects.filter(Q(nutritional_status=uw) | Q(nutritional_status=suw)).filter(
            opt__date__year=year_now).filter(opt__barangay=b).aggregate(sum=Sum('values'))['sum']
        data[b.name] = int(total)

    a = max(data.items(), key=operator.itemgetter(1))[0]
    tops.append(a)

    # W and SW
    uw = NutritionalStatus.objects.get(name__contains='Weight for Height/Length - Wasted')
    suw = NutritionalStatus.objects.get(name__contains='Weight for Height/Length - Severely Wasted')

    data = {}

    for b in barangays:
        total = OPTValues.objects.filter(Q(nutritional_status=uw) | Q(nutritional_status=suw)).filter(
            opt__date__year=year_now).filter(opt__barangay=b).aggregate(sum=Sum('values'))['sum']
        data[b.name] = int(total)

    a = max(data.items(), key=operator.itemgetter(1))[0]
    tops.append(a)

    return tops


# count per barangay per category
def count_per_barangay_per_category():

    data = []
    for b in Barangay.objects.all():
        sub_data = []
        sub_data.append(b.name)

        uw = NutritionalStatus.objects.get(name__contains='Weight for Age - Underweight')
        suw = NutritionalStatus.objects.get(name__contains='Weight for Age - Severely Underweight')

        total = OPTValues.objects.filter(Q(nutritional_status=uw) | Q(nutritional_status=suw)).filter(
            opt__date__year=year_now).filter(opt__barangay=b).aggregate(sum=Sum('values'))['sum']
        sub_data.append(total)

        uw = NutritionalStatus.objects.get(name__contains='Height for Age - Stunted')
        suw = NutritionalStatus.objects.get(name__contains='Height for Age - Severely Stunted')

        total = OPTValues.objects.filter(Q(nutritional_status=uw) | Q(nutritional_status=suw)).filter(
            opt__date__year=year_now).filter(opt__barangay=b).aggregate(sum=Sum('values'))['sum']
        sub_data.append(total)

        uw = NutritionalStatus.objects.get(name__contains='Weight for Height/Length - Wasted')
        suw = NutritionalStatus.objects.get(name__contains='Weight for Height/Length - Severely Wasted')

        total = OPTValues.objects.filter(Q(nutritional_status=uw) | Q(nutritional_status=suw)).filter(
            opt__date__year=year_now).filter(opt__barangay=b).aggregate(sum=Sum('values'))['sum']
        sub_data.append(total)

        data.append(sub_data)

    return data


# highcharts highest 3

def highest_barangay_per_category_json():

    barangays = Barangay.objects.all()

    data = {}

    uw = NutritionalStatus.objects.get(name__contains='Weight for Age - Underweight')
    suw = NutritionalStatus.objects.get(name__contains='Weight for Age - Severely Underweight')

    # S and SS
    s = NutritionalStatus.objects.get(name__contains='Height for Age - Stunted')
    ss = NutritionalStatus.objects.get(name__contains='Height for Age - Severely Stunted')

    # W and SW
    ws = NutritionalStatus.objects.get(name__contains='Weight for Height/Length - Wasted')
    sws = NutritionalStatus.objects.get(name__contains='Weight for Height/Length - Severely Wasted')

    for b in barangays:
        total = OPTValues.objects.filter(Q(nutritional_status=uw) | Q(nutritional_status=suw) |
                                         Q(nutritional_status=s) | Q(nutritional_status=ss) |
                                         Q(nutritional_status=ws) | Q(nutritional_status=sws)).filter(
            opt__date__year=year_now).filter(opt__barangay=b).aggregate(sum=Sum('values'))['sum']
        data[b.name] = int(total)

    barangay_names = sorted(data, key=data.get, reverse=True)[:3]

    json_data = {
        'barangays': [b.name for b in barangays]
    }

    # return /list/ of values

    # UW and SUW
    first_list = []
    for b in barangay_names:
        bar = Barangay.objects.get(name=b)
        total = OPTValues.objects.filter(opt__barangay=bar, opt__date__year=year_now).filter(
            Q(nutritional_status=uw) | Q(nutritional_status=suw)
        ).aggregate(sum=Sum('values'))['sum']

        first_list.append(int(total))

    second_list = []
    for b in barangay_names:
        bar = Barangay.objects.get(name=b)
        total = OPTValues.objects.filter(opt__barangay=bar, opt__date__year=year_now).filter(
            Q(nutritional_status=s) | Q(nutritional_status=ss)
        ).aggregate(sum=Sum('values'))['sum']

        second_list.append(int(total))

    third_list = []
    for b in barangay_names:
        bar = Barangay.objects.get(name=b)
        total = OPTValues.objects.filter(opt__barangay=bar, opt__date__year=year_now).filter(
            Q(nutritional_status=ws) | Q(nutritional_status=sws)
        ).aggregate(sum=Sum('values'))['sum']

        third_list.append(int(total))

    json_data['first'] = first_list
    json_data['second'] = second_list
    json_data['third'] = third_list

    return json_data


# # # # # # # # # REPORT # # # # # # # # # #

def report_table():

    grand_data = []
    data = []
    male = Sex.objects.get(name='Male')
    female = Sex.objects.get(name='Female')

    barangays = Barangay.objects.all().order_by('name')

    # Weight for Age
    wfa_normal = NutritionalStatus.objects.get(name='Weight for Age - Normal')
    wfa_uw = NutritionalStatus.objects.get(name='Weight for Age - Underweight')
    wfa_suw = NutritionalStatus.objects.get(name='Weight for Age - Severely Underweight')
    wfa_ow = NutritionalStatus.objects.get(name='Weight for Age - Overweight')

    for b in barangays:

        query = OPTValues.objects.filter(opt__date__year=year_now, opt__barangay=b)
        sub_data = [b.name]

        # get the normal
        nboys = query.filter(age_group__sex=male, nutritional_status=wfa_normal).aggregate(sum=Sum('values'))['sum']
        ngirls = query.filter(age_group__sex=female, nutritional_status=wfa_normal).aggregate(sum=Sum('values'))['sum']
        ntotal = nboys + ngirls

        sub_data.append(nboys)
        sub_data.append(ngirls)
        sub_data.append(ntotal)

        # get the underweight
        nboys = query.filter(age_group__sex=male, nutritional_status=wfa_uw).aggregate(sum=Sum('values'))['sum']
        ngirls = query.filter(age_group__sex=female, nutritional_status=wfa_uw).aggregate(sum=Sum('values'))['sum']
        ntotal = nboys + ngirls

        sub_data.append(nboys)
        sub_data.append(ngirls)
        sub_data.append(ntotal)

        # get the suw
        nboys = query.filter(age_group__sex=male, nutritional_status=wfa_suw).aggregate(sum=Sum('values'))['sum']
        ngirls = query.filter(age_group__sex=female, nutritional_status=wfa_suw).aggregate(sum=Sum('values'))['sum']
        ntotal = nboys + ngirls

        sub_data.append(nboys)
        sub_data.append(ngirls)
        sub_data.append(ntotal)

        # get the ow
        nboys = query.filter(age_group__sex=male, nutritional_status=wfa_ow).aggregate(sum=Sum('values'))['sum']
        ngirls = query.filter(age_group__sex=female, nutritional_status=wfa_ow).aggregate(sum=Sum('values'))['sum']
        ntotal = nboys + ngirls

        sub_data.append(nboys)
        sub_data.append(ngirls)
        sub_data.append(ntotal)

        # total per barangay
        barangay_total = query.aggregate(sum=Sum('values'))['sum']
        sub_data.append(barangay_total)

        uw_suw = query.filter(Q(nutritional_status=wfa_uw) | Q(nutritional_status=wfa_suw)).aggregate(sum=Sum('values'))['sum']
        sub_data.append(uw_suw)
        sub_data.append(round(uw_suw / barangay_total, 2))

        data.append(sub_data)
    grand_data.append(data)

    data = []
    # Height for Age
    hfa_normal = NutritionalStatus.objects.get(name='Height for Age - Normal')
    hfa_s = NutritionalStatus.objects.get(name='Height for Age - Stunted')
    hfa_ss = NutritionalStatus.objects.get(name='Height for Age - Severely Stunted')
    hfa_t = NutritionalStatus.objects.get(name='Height for Age - Tall')

    for b in barangays:

        query = OPTValues.objects.filter(opt__date__year=year_now, opt__barangay=b)
        sub_data = [b.name]

        # get the normal
        nboys = query.filter(age_group__sex=male, nutritional_status=hfa_normal).aggregate(sum=Sum('values'))['sum']
        ngirls = query.filter(age_group__sex=female, nutritional_status=hfa_normal).aggregate(sum=Sum('values'))['sum']
        ntotal = nboys + ngirls

        sub_data.append(nboys)
        sub_data.append(ngirls)
        sub_data.append(ntotal)

        # get the stunted
        nboys = query.filter(age_group__sex=male, nutritional_status=hfa_s).aggregate(sum=Sum('values'))['sum']
        ngirls = query.filter(age_group__sex=female, nutritional_status=hfa_s).aggregate(sum=Sum('values'))['sum']
        ntotal = nboys + ngirls

        sub_data.append(nboys)
        sub_data.append(ngirls)
        sub_data.append(ntotal)

        # get the severely stunted
        nboys = query.filter(age_group__sex=male, nutritional_status=hfa_ss).aggregate(sum=Sum('values'))['sum']
        ngirls = query.filter(age_group__sex=female, nutritional_status=hfa_ss).aggregate(sum=Sum('values'))['sum']
        ntotal = nboys + ngirls

        sub_data.append(nboys)
        sub_data.append(ngirls)
        sub_data.append(ntotal)

        # get the tall
        nboys = query.filter(age_group__sex=male, nutritional_status=hfa_t).aggregate(sum=Sum('values'))['sum']
        ngirls = query.filter(age_group__sex=female, nutritional_status=hfa_t).aggregate(sum=Sum('values'))['sum']
        ntotal = nboys + ngirls

        sub_data.append(nboys)
        sub_data.append(ngirls)
        sub_data.append(ntotal)

        # total per barangay
        barangay_total = query.aggregate(sum=Sum('values'))['sum']
        sub_data.append(barangay_total)

        uw_suw = query.filter(Q(nutritional_status=hfa_s) | Q(nutritional_status=hfa_ss)).aggregate(sum=Sum('values'))['sum']
        sub_data.append(uw_suw)
        sub_data.append(round(uw_suw / barangay_total, 2))

        data.append(sub_data)
    grand_data.append(data)

    data = []
    # Weight for Height / Length
    wfh_normal = NutritionalStatus.objects.get(name='Weight for Height/Length - Normal')
    wfh_wasted = NutritionalStatus.objects.get(name='Weight for Height/Length - Wasted')
    wfh_sw = NutritionalStatus.objects.get(name='Weight for Height/Length - Severely Wasted')
    wfh_obese = NutritionalStatus.objects.get(name='Weight for Height/Length - Obese')
    wfh_ow = NutritionalStatus.objects.get(name='Weight for Height/Length - Overweight')

    for b in barangays:

        query = OPTValues.objects.filter(opt__date__year=year_now, opt__barangay=b)
        sub_data = [b.name]

        # get the normal
        nboys = query.filter(age_group__sex=male, nutritional_status=wfh_normal).aggregate(sum=Sum('values'))['sum']
        ngirls = query.filter(age_group__sex=female, nutritional_status=wfh_normal).aggregate(sum=Sum('values'))['sum']
        ntotal = nboys + ngirls

        sub_data.append(nboys)
        sub_data.append(ngirls)
        sub_data.append(ntotal)

        # get the wasted
        nboys = query.filter(age_group__sex=male, nutritional_status=wfh_wasted).aggregate(sum=Sum('values'))['sum']
        ngirls = query.filter(age_group__sex=female, nutritional_status=wfh_wasted).aggregate(sum=Sum('values'))['sum']
        ntotal = nboys + ngirls

        sub_data.append(nboys)
        sub_data.append(ngirls)
        sub_data.append(ntotal)

        # get the sw
        nboys = query.filter(age_group__sex=male, nutritional_status=wfh_sw).aggregate(sum=Sum('values'))['sum']
        ngirls = query.filter(age_group__sex=female, nutritional_status=wfh_sw).aggregate(sum=Sum('values'))['sum']
        ntotal = nboys + ngirls

        sub_data.append(nboys)
        sub_data.append(ngirls)
        sub_data.append(ntotal)

        # get the ow
        nboys = query.filter(age_group__sex=male, nutritional_status=wfh_ow).aggregate(sum=Sum('values'))['sum']
        ngirls = query.filter(age_group__sex=female, nutritional_status=wfh_ow).aggregate(sum=Sum('values'))['sum']
        ntotal = nboys + ngirls

        sub_data.append(nboys)
        sub_data.append(ngirls)
        sub_data.append(ntotal)

        # get the obese
        nboys = query.filter(age_group__sex=male, nutritional_status=wfh_obese).aggregate(sum=Sum('values'))['sum']
        ngirls = query.filter(age_group__sex=female, nutritional_status=wfh_obese).aggregate(sum=Sum('values'))['sum']
        ntotal = nboys + ngirls

        sub_data.append(nboys)
        sub_data.append(ngirls)
        sub_data.append(ntotal)

        # total per barangay
        barangay_total = query.aggregate(sum=Sum('values'))['sum']
        sub_data.append(barangay_total)

        uw_suw = query.filter(Q(nutritional_status=wfh_wasted) | Q(nutritional_status=wfh_sw)).aggregate(sum=Sum('values'))['sum']
        sub_data.append(uw_suw)
        sub_data.append(round(uw_suw / barangay_total, 2))

        data.append(sub_data)
    grand_data.append(data)

    return grand_data


