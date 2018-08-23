
import decimal
import json
import random
import string
from datetime import datetime
from tkinter import N

from friends.datapreprocessing import helper
from django.apps import apps
from django.db.models import Sum, Avg, Count
from computations.weights import year_now
from friends.datamining import forecast, correlations
from computations import weights
from datainput.models import ChildCare, FamilyProfileLine, MaternalCare, Malaria, Immunization, Tuberculosis, Barangay, \
    InformalSettlers
from friends import datapoints, general, revised_datapoints
from friends.datapreprocessing import consolidators
from django.db import models

# Create your models here.
from friends.datapreprocessing.consolidators import get_field


class Metric(models.Model):

    metric = models.CharField(max_length=150)
    threshold = models.DecimalField(max_digits=10, decimal_places=2)

    UNIT_CHOICES = (
        ('Total', 'Total'),
        ('Rate', 'Rate')
    )
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='Total')
    date = models.DateTimeField(default=datetime.now)
    is_completed = models.BooleanField(default=False)
    is_default = models.BooleanField(default=True)
    threshold_bad = models.BooleanField(default=True, verbose_name='Is Value Reaching Threshold Bad')
    json_data = models.TextField(default='')


    @staticmethod
    def categorized():

        illnesses = [metric for metric in Metric.objects.filter(metric__contains='Child Care')]
        maternal = [metric for metric in Metric.objects.filter(metric__contains='Maternal Care')]
        socioeconomic = [metric for metric in Metric.objects.filter(metric__contains='Family Profile')]

        return {
            'illnesses': illnesses,
            'maternal': maternal,
            'socioeconomic': socioeconomic
        }

    @staticmethod
    def to_metric(data):
        try:
            metric = Metric.objects.get(metric=data)
            return metric
        except Metric.DoesNotExist:
            return None

    @property
    def to_highcharts(self):

        values = eval(self.get_value_until_present)
        years = sorted([key for key, value in values.items()])
        data = [value for key, value in values.items()]

        return [years, data]

    def get_related_data_points(self):

        # illnesses

        if self.get_data_point == 'Number of Anemic children':
            brothers = [field for field in revised_datapoints.ILLNESSES if field != self.get_data_point]
            brothers.append('Number of children who received iron')
            brothers.append('Number of children who received vitamin A')
            brothers.append('Number of children who received MNP')

            return brothers

        if self.get_data_point == 'Number of Diarrhea cases':
            brothers = [field for field in revised_datapoints.ILLNESSES if field != self.get_data_point]
            brothers.append('Number of Children Given ROTA')
            brothers.append('Number of children who received vitamin A')


            return brothers

        if self.get_data_point == 'Number of Pneumonia cases':
            brothers = [field for field in revised_datapoints.ILLNESSES if field != self.get_data_point]
            brothers.append('Number of Children Given PENTA')
            brothers.append('Number of Children Given PCV')

            return brothers

        if self.get_data_point == 'Number of Dengue Cases':
            brothers = [field for field in revised_datapoints.ILLNESSES if field != self.get_data_point]
            brothers.append('Number of families using a Well as water source')

            return brothers

        if self.get_data_point == 'Number of Children with Hepatitis':
            brothers = [field for field in revised_datapoints.ILLNESSES if field != self.get_data_point]
            brothers.append('Number of Children Given HEPA')

            return brothers

        if self.get_data_point == 'Number of Children with Measles':
            brothers = [field for field in revised_datapoints.ILLNESSES if field != self.get_data_point]
            brothers.append('Number of Children Given MCV')

            return brothers

        if self.get_data_point == 'Number of Tuberculosis Identified':
            brothers = [field for field in revised_datapoints.ILLNESSES if field != self.get_data_point]
            brothers.append('Number of Children Given BCG')

            return brothers

        if self.get_data_point == 'Number of Malaria Cases':
            brothers = [field for field in revised_datapoints.ILLNESSES if field != self.get_data_point]
            brothers.append('Number of families using a Well as water source')

            return brothers

        # socioeconomic
        if self.get_data_point == 'Number of families using a Well as water source':
            return [
                'Number of Malaria Cases',
                'Number of Dengue Cases'
            ]

        if self.get_data_point == 'Number of families using an Open Pit toilet type':
            return [
                'Number of Tuberculosis Identified',
                'Number of Diarrhea cases'
            ]

        if self.get_data_point == 'Number of families who do not have toilets':
            return [
                'Number of Tuberculosis Identified',
                'Number of Diarrhea cases'
            ]

        if self.get_data_point == 'Number of Elementary Undergraduate Parents':
            return [
                'Number of mothers practicing exclusive breastfeeding'
            ]

        if self.get_data_point == 'Number of families practicing Family Planning':
            return [
                'Number of mothers practicing exclusive breastfeeding'
            ]

        if self.get_data_point == 'Number of families using iodized salt':
            return [
                'Number of Elementary Undergraduate Parents'
            ]

        # maternal
        if self.get_data_point == 'Number of mothers practicing exclusive breastfeeding':
            return [
                'Number of mothers who have children with low birth weight'

            ]

        if self.get_data_point == 'Number of mothers who have children with low birth weight':
            return [
                'Number of mothers practicing exclusive breastfeeding'
            ]

        if self.get_data_point == 'Number of Pregnant women with 4 or more prenatal visits':
            return []
        if self.get_data_point == 'Number of Pregnant women given 2 doses of Tetanus Toxoid':
            return []
        if self.get_data_point == 'Number of Postpartum women with at least 2 postpartum visits':
            return []
        if self.get_data_point == 'Number of Pregnant women given TT2 plus':
            return []
        if self.get_data_point == 'Number of Pregnant women given complete iron with folic acid supplementation':
            return []
        if self.get_data_point == 'Number of Postpartum women with given complete iron supplementation':
            return []
        if self.get_data_point == 'Number of Postpartum women given Vitamin A supplementation':
            return []

        # immunizations
        if self.get_data_point == 'Number of Children Given BCG':
            return []
        if self.get_data_point == 'Number of Children Given HEPA':
            return []
        if self.get_data_point == 'Number of Children Given PENTA':
            return []
        if self.get_data_point == 'Number of Children Given OPV':
            return []
        if self.get_data_point == 'Number of Children Given MCV':
            return []
        if self.get_data_point == 'Number of Children Given ROTA':
            return []
        if self.get_data_point == 'Number of Children Given PCV':
            return []

        # micronutrient
        if self.get_data_point == 'Number of children who received vitamin A':
            return []
        if self.get_data_point == 'Number of children who received iron':
            return []
        if self.get_data_point == 'Number of children who received MNP':
            return []

        if self.get_data_point == 'Number of Informal Families':
            return []

        return []

    def get_correlations(self):

        data = []

        for field in self.get_related_data_points():
            other = helper.get_value_until_present(helper.get_source(field), field)
            variables = correlations.make_variables(eval(self.get_value_until_present), eval(other))
            score = correlations.get_correlation_score(variables)
            # data.append([field, variables, score])
            data.append({
                'field': field,
                'variables': variables,
                'score': score,
                'remark': correlations.get_correlation_remark(score)
            })

        return data

    def get_insights(self):

        data = []
        for field in self.get_related_data_points():
            source = helper.get_source(field)
            my_dict = helper.get_value_until_present(source, field)

            variables = correlations.make_variables(eval(self.get_value_until_present), eval(my_dict))
            score = correlations.get_correlation_score(variables)

            data.append({
                'distribution': helper.get_distribution_per_barangay(source, field),
                'trend': helper.to_high_charts(my_dict),
                'field': field,
                'id': helper.id_generator(6),
                'score': score,
                'remark': correlations.get_correlation_remark(score),
                'start': 2015
            })

        return data

    @property
    def get_distribution_per_barangay(self):

        if self.get_source == 'Family Profile':
            query = FamilyProfileLine.objects.filter(family_profile__date__year=year_now)

            if self.get_data_point == 'Number of families using a Well as water source':

                data = []
                for barangay in Barangay.objects.all():
                    total = query.filter(family_profile__barangay=barangay).filter(water_sources='Well').count()
                    data.append([barangay.name, int(total)])

                return data

            if self.get_data_point == 'Number of families using an Open Pit toilet type':

                data = []
                for barangay in Barangay.objects.all():
                    total = query.filter(family_profile__barangay=barangay).filter(toilet_type='Open Pit').count()
                    data.append([barangay.name, int(total)])

                return data

            if self.get_data_point == 'Number of families who do not have toilets':

                data = []
                for barangay in Barangay.objects.all():
                    total = query.filter(family_profile__barangay=barangay).filter(toilet_type='None').count()
                    data.append([barangay.name, int(total)])

                return data

            if self.get_data_point == 'Number of Elementary Undergraduate Parents':

                data = []
                for barangay in Barangay.objects.all():
                    total = query.filter(family_profile__barangay=barangay).filter(educational_attainment='Elementary Undergraduate').count()
                    data.append([barangay.name, int(total)])

                return data

            if self.get_data_point == 'Number of families using iodized salt':

                data = []
                for barangay in Barangay.objects.all():
                    total = query.filter(family_profile__barangay=barangay).filter(is_using_iodized_salt=True).count()
                    data.append([barangay.name, int(total)])

                return data

            if self.get_data_point == 'Number of families practicing Family Planning':

                data = []
                for barangay in Barangay.objects.all():
                    total = query.filter(family_profile__barangay=barangay).filter(is_family_planning=True).count()
                    data.append([barangay.name, int(total)])

                return data

        trimmed = self.get_source.replace(' ', '')
        model = apps.get_model('datainput', trimmed)

        field = get_field(model, self.get_data_point)
        query = model.objects.all().filter(fhsis__date__year=year_now)

        data = []
        for barangay in Barangay.objects.all():
            total = query.filter(fhsis__barangay=barangay).aggregate(sum=Sum(field))['sum']
            data.append([barangay.name, int(total)])

        return data

    def to_high_charts_d(self):

        data = self.get_distribution_per_barangay

        fields = [x[0] for x in data]
        values = [x[1] for x in data]

        return {
            'fields': fields,
            'values': values
        }

    @property
    def get_value_until_present(self):

        point = self.get_data_point.strip()

        # hard coded
        if point == revised_datapoints.SOCIOECONOMIC[0]: point = 'Well'
        elif point == revised_datapoints.SOCIOECONOMIC[1]: point = 'Open Pit'
        elif point == revised_datapoints.SOCIOECONOMIC[2]: point = 'None'
        elif point == revised_datapoints.SOCIOECONOMIC[3]: point = 'Elementary Undergraduate'
        elif point == revised_datapoints.SOCIOECONOMIC[4]: point = 'Number of families practicing family planning'
        elif point == revised_datapoints.SOCIOECONOMIC[5]: point = 'Number of families using iodized salt'

        if self.get_source.strip() == 'Family Profile':

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

            field = consolidators.get_field(FamilyProfileLine, self.get_data_point.strip())
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

        elif self.get_source.strip() == 'Maternal Care':

            field = consolidators.get_field(MaternalCare, self.get_data_point.strip())
            start_year = [d.year for d in MaternalCare.objects.all().dates('fhsis__date', 'year')][0]

            data = {}
            while start_year <= weights.year_now:
                data[start_year] = float(MaternalCare.objects.filter(fhsis__date__year=start_year).aggregate(sum=Sum(field))['sum'])
                start_year += 1

            return json.dumps(data)

        elif self.get_source.strip() == 'Child Care':

            field = consolidators.get_field(ChildCare, self.get_data_point.strip())
            start_year = [d.year for d in
                           ChildCare.objects.all().dates('fhsis__date', 'year')][0]

            data = {}
            while start_year <= weights.year_now:
                data[start_year] = float(ChildCare.objects.filter(fhsis__date__year=start_year).aggregate(
                    sum=Sum(field))['sum'])
                start_year += 1

            return json.dumps(data)

        elif self.get_source.strip() == 'Malaria':

            field = consolidators.get_field(Malaria, self.get_data_point.strip())
            start_year = [d.year for d in
                           Malaria.objects.all().dates('fhsis__date', 'year')][0]

            data = {}
            while start_year <= weights.year_now:
                data[start_year] = float(Malaria.objects.filter(fhsis__date__year=start_year).aggregate(
                    sum=Sum(field))['sum'])
                start_year += 1

            return json.dumps(data)

        elif self.get_source.strip() == 'Immunization':

            field = consolidators.get_field(Immunization, self.get_data_point.strip())
            start_year = [d.year for d in
                           Immunization.objects.all().dates('fhsis__date', 'year')][0]

            data = {}
            while start_year <= weights.year_now:
                data[start_year] = float(Immunization.objects.filter(fhsis__date__year=start_year).aggregate(
                    sum=Sum(field))['sum'])
                start_year += 1

            return json.dumps(data)

        elif self.get_source.strip() == 'Tuberculosis':

            field = consolidators.get_field(Tuberculosis, self.get_data_point.strip())
            start_year = [d.year for d in
                           Tuberculosis.objects.all().dates('fhsis__date', 'year')][0]

            data = {}
            while start_year <= weights.year_now:
                data[start_year] = float(Tuberculosis.objects.filter(fhsis__date__year=start_year).aggregate(
                    sum=Sum(field))['sum'])
                start_year += 1

            return json.dumps(data)

    @staticmethod
    def check_if_set(name):

        for metric in Metric.objects.all():
            if metric.get_data_point == name:
                return True

        return False

    @property
    def get_prevalence_rate(self):

        total_population = weights.get_total_population(year_now)
        return round((self.get_total_value / total_population) * 100, 2)

    def __str__(self):
        return self.metric

    @property
    def get_type(self):
        if self.threshold_bad:
            return "is greater than"
        return "is less than"

    @property
    def is_alarming(self):

        if self.threshold_bad:
            return float(self.get_total_value) > float(self.threshold)

        return float(self.get_total_value) < float(self.threshold)

    @property
    def is_supplement(self):

        supplements = [
            'Given complimentary food',
            'Children given deworming',
            'Anemic children receiving full dose iron',
            'Infants who received vitamin A',
            'Infants who received iron',
            'Infants who received MNP',
            'Pregnant women given 2 doses of Tetanus Toxoid',
            'Pregnant women given TT2 plus',
            'Pregnant women given complete iron with folic acid supplementation',
            'Postpartum women with given complete iron supplementation',
            'Postpartum women given Vitamin A supplementation',
            'Given BCG',
            'Given HEPA',
            'Given PENTA',
            'Given OPV',
            'Given MCV',
            'Given ROTA',
            'Given PCV',
        ]

        return self.get_data_point.strip() in supplements

    @staticmethod
    def get_supplement_metrics():

        return [metric for metric in Metric.objects.all() if metric.is_supplement]

    @property
    def get_total_value(self):
        return consolidators.get_value(self.metric)

    @property
    def get_total_average(self):

        point = self.get_data_point.strip()
        year_now = datetime.now().year

        if self.get_source.strip() == 'Family Profile':

            if point in datapoints.water_sources:

                return FamilyProfileLine.objects.filter(family_profile__date__year=year_now,
                                                             water_sources=point).count()

            if point in datapoints.food_production:

                return FamilyProfileLine.objects.filter(family_profile__date__year=year_now,
                                                        food_production_activity=point).count()

            if point in datapoints.educational_attainment_for_r:

                return FamilyProfileLine.objects.filter(family_profile__date__year=year_now,
                                                             educational_attainment=point).count()

            if point in datapoints.toilet_type:

                return FamilyProfileLine.objects.filter(family_profile__date__year=year_now,
                                                             toilet_type=point).count()

            # for booleans

            field = consolidators.get_field(FamilyProfileLine, self.get_data_point.strip())
            count = 0
            for f in FamilyProfileLine.objects.filter(family_profile__date__year=year_now):
                if getattr(f, field):
                    count = count + 1

            return count

        elif self.get_source.strip() == 'Maternal Care':

            field = consolidators.get_field(MaternalCare, self.get_data_point.strip())
            return float(MaternalCare.objects.filter(fhsis__date__year=weights.year_now).aggregate(avg=Avg(field))['avg'])

        elif self.get_source.strip() == 'Child Care':

            field = consolidators.get_field(ChildCare, self.get_data_point.strip())
            return float(ChildCare.objects.filter(fhsis__date__year=weights.year_now).aggregate(
                        avg=Avg(field))['avg'])

        elif self.get_source.strip() == 'Malaria':

            field = consolidators.get_field(Malaria, self.get_data_point.strip())
            return float(
                    Malaria.objects.filter(fhsis__date__year=weights.year_now).aggregate(
                        avg=Avg(field))['avg'])

        elif self.get_source.strip() == 'Immunization':

            field = consolidators.get_field(Immunization, self.get_data_point.strip())
            return float(
                    Immunization.objects.filter(fhsis__date__year=weights.year_now).aggregate(
                        avg=Avg(field))['avg'])

        elif self.get_source.strip() == 'Tuberculosis':

            field = consolidators.get_field(Tuberculosis, self.get_data_point.strip())
            return float(
                    Tuberculosis.objects.filter(fhsis__date__year=weights.year_now).aggregate(
                        avg=Avg(field))['avg'])

    @property
    def get_source(self):

        phrase = self.metric.split("|")
        return phrase[0].strip()

    @property
    def get_data_point(self):

        try:
            phrase = self.metric.split("|")
            return phrase[1].strip()
        except IndexError:
            return 'Unemployment Rate'

    @property
    def get_sex(self):

        try:
            phrase = self.metric.split("|")
            return phrase[2].strip()
        except IndexError:
            return 'N/A'

    @property
    def get_document(self):

        phrase = self.metric.strip().split("|")
        model = 'default'
        first = phrase[0]

        if len(phrase) == 2:

            if 'Maternal Care' in first:
                return 'FHSIS'
            elif 'STI Surveillance' in first:
                model = 'STISurveillance'
            elif 'Family Profile' in first:
                model = 'Family Profile'
            elif 'Health Care Waste Management' in first:
                model = 'HealthCareWasteManagement'
            elif 'InformalSettlers' in first:
                model = 'Informal Settlers'
            elif 'Nutritional Status' in first:
                return 'OPTValues'
            elif 'Child Care' in first:
                return 'FHSIS'
            elif 'Malaria' in first:
                return 'FHSIS'
            elif 'Tuberculosis' in first:
                return 'FHSIS'
            elif 'Immunization' in first:
                return 'FHSIS'

        elif len(phrase) == 1:

            if 'Unemployment Rate' in first:
                model = 'UnemploymentRate'

        elif len(phrase) == 3:

            if 'Nutritional Status' in first:
                return 'OPTValues'
            else:
                return first.replace(' ', '')

        return model

    @staticmethod
    def get_alarming():

        return [x for x in Metric.objects.all() if x.is_alarming]

    @staticmethod
    def get_critical_non_supplements():

        return [metric for metric in Metric.get_alarming() if not metric.is_supplement]

    @staticmethod
    def get_critical_supplements():

        return [metric for metric in Metric.get_alarming() if metric.is_supplement]

    def to_dict(self):
        return {
            'field': self.get_data_point,
            'threshold': int(self.threshold),
            'value': int(self.get_total_value),
            'is_alarming': self.get_total_value >= self.threshold
        }

    @property
    def is_predicted_critical(self):

        dict = self.get_average_over_time
        data = [round(value, 2) for key, value in dict.items()]

        weighted_average = forecast.get_weighted_moving_average(data)

        if self.threshold_bad:
            return float(weighted_average) > float(self.threshold)

        return float(weighted_average) < float(self.threshold)

    @property
    def predicted_value(self): # for next time period
        dict = self.get_average_over_time
        data = [round(value, 2) for key, value in dict.items()]

        return forecast.get_weighted_moving_average(data)

    @property
    def get_average_over_time(self):

        point = self.get_data_point.strip()

        if self.get_source.strip() == 'Family Profile':

            if point in datapoints.water_sources:
                start_year = [d.year for d in FamilyProfileLine.objects.dates('family_profile__date', 'year')][0]

                data = {}
                while start_year <= weights.year_now:
                    count = FamilyProfileLine.objects.filter(family_profile__date__year=start_year,
                                                             water_sources=point).count()

                    data[start_year] = count
                    start_year = start_year + 1

                return data

            if point in datapoints.food_production:
                start_year = [d.year for d in FamilyProfileLine.objects.dates('family_profile__date', 'year')][0]

                data = {}
                while start_year <= weights.year_now:
                    count = FamilyProfileLine.objects.filter(family_profile__date__year=start_year,
                                                             food_production_activity=point).count()

                    data[start_year] = count
                    start_year = start_year + 1

                return data

            if point in datapoints.educational_attainment_for_r:
                start_year = [d.year for d in FamilyProfileLine.objects.dates('family_profile__date', 'year')][0]

                data = {}
                while start_year <= weights.year_now:
                    count = FamilyProfileLine.objects.filter(family_profile__date__year=start_year,
                                                             educational_attainment=point).count()

                    data[start_year] = count
                    start_year = start_year + 1

                return data

            if point in datapoints.toilet_type:
                start_year = [d.year for d in FamilyProfileLine.objects.dates('family_profile__date', 'year')][0]

                data = {}
                while start_year <= weights.year_now:
                    count = FamilyProfileLine.objects.filter(family_profile__date__year=start_year,
                                                             toilet_type=point).count()

                    data[start_year] = count
                    start_year = start_year + 1

                return data

            field = consolidators.get_field(FamilyProfileLine, self.get_data_point.strip())
            start_year = [d.year for d in FamilyProfileLine.objects.dates('family_profile__date', 'year')][0]

            data = {}
            while start_year <= weights.year_now:

                count = 0
                for f in FamilyProfileLine.objects.filter(family_profile__date__year=start_year):
                    if getattr(f, field):
                        count = count + 1

                data[start_year] = count
                start_year = start_year + 1

            return data

        elif self.get_source.strip() == 'Maternal Care':

            field = consolidators.get_field(MaternalCare, self.get_data_point.strip())
            start_month = [d.month for d in
                           MaternalCare.objects.filter(fhsis__date__year=weights.year_now).dates('fhsis__date',
                                                                                                 'month')][0]

            data = {}
            while start_month <= weights.month_now:
                data[general.month_converter(start_month)] = float(
                    MaternalCare.objects.filter(fhsis__date__year=weights.year_now,
                                                fhsis__date__month=start_month).aggregate(avg=Avg(field))['avg'])
                start_month = start_month + 1

            return data

        elif self.get_source.strip() == 'Child Care':

            field = consolidators.get_field(ChildCare, self.get_data_point.strip())
            start_month = [d.month for d in
                           ChildCare.objects.filter(fhsis__date__year=weights.year_now).dates('fhsis__date',
                                                                                              'month')][0]

            data = {}
            while start_month <= weights.month_now:
                data[general.month_converter(start_month)] = float(
                    ChildCare.objects.filter(fhsis__date__year=weights.year_now,
                                             fhsis__date__month=start_month).aggregate(
                        avg=Avg(field))['avg'])
                start_month = start_month + 1

            return data

        elif self.get_source.strip() == 'Malaria':

            field = consolidators.get_field(Malaria, self.get_data_point.strip())
            start_month = [d.month for d in
                           Malaria.objects.filter(fhsis__date__year=weights.year_now).dates('fhsis__date',
                                                                                            'month')][0]

            data = {}
            while start_month <= weights.month_now:
                data[general.month_converter(start_month)] = float(
                    Malaria.objects.filter(fhsis__date__year=weights.year_now,
                                           fhsis__date__month=start_month).aggregate(
                        avg=Avg(field))['avg'])
                start_month = start_month + 1

            return data

        elif self.get_source.strip() == 'Immunization':

            field = consolidators.get_field(Immunization, self.get_data_point.strip())
            start_month = [d.month for d in
                           Immunization.objects.filter(fhsis__date__year=weights.year_now).dates('fhsis__date',
                                                                                                 'month')][0]

            data = {}
            while start_month <= weights.month_now:
                data[general.month_converter(start_month)] = float(
                    Immunization.objects.filter(fhsis__date__year=weights.year_now,
                                                fhsis__date__month=start_month).aggregate(
                        avg=Avg(field))['avg'])
                start_month = start_month + 1

            return data

        elif self.get_source.strip() == 'Tuberculosis':

            field = consolidators.get_field(Tuberculosis, self.get_data_point.strip())
            start_month = [d.month for d in
                           Tuberculosis.objects.filter(fhsis__date__year=weights.year_now).dates('fhsis__date',
                                                                                                 'month')][0]

            data = {}
            while start_month <= weights.month_now:
                data[general.month_converter(start_month)] = float(
                    Tuberculosis.objects.filter(fhsis__date__year=weights.year_now,
                                                fhsis__date__month=start_month).aggregate(
                        avg=Avg(field))['avg'])
                start_month = start_month + 1

            return data

    @staticmethod
    def get_nutritional_status_by_category(category):

        metrics = []

        data = [metric.to_dict() for metric in Metric.objects.all() if metric.get_source == 'Nutritional Status' and metric.is_default]

        for d in data:
            if category == d['field'].split('-')[0].strip():
                metrics.append(d)

        return metrics

    @staticmethod
    def get_micronutrient():

        data = [metric.to_dict() for metric in Metric.objects.all() if
                metric.get_source == 'Child Care' and metric.get_data_point in datapoints.micronutrient
                                                  and metric.is_default]

        return data

    @staticmethod
    def get_maternal():

        data = [metric.to_dict() for metric in Metric.objects.all() if metric.get_source == 'Maternal Care'
                and metric.get_data_point in datapoints.maternal and metric.is_default]

        return data

    @staticmethod
    def get_child_care():

        return [metric.to_dict() for metric in Metric.objects.all()
                if metric.get_source == 'Child Care' and metric.get_data_point in datapoints.child_care
                and metric.is_default]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # COMPUTATION # # # #

    @staticmethod
    def get_sum_nutritional_status(status):

        total = 0
        for m in Metric.objects.filter(is_default=True):
            if m.get_data_point == status:
                total = total + m.get_total_value

        return float(total)

    @staticmethod
    def get_total_per_category(category):

        total = 0
        for m in Metric.objects.filter(is_default=True):
            if m.get_source == 'Nutritional Status':
                cat = m.get_data_point.strip().split("-")[0]
                if cat == category:
                    total = total + m.get_total_value

        return float(total)

    @staticmethod
    def get_computations_nutritional_status(status):

        sum = Metric.get_sum_nutritional_status(status)
        category = status.strip().split("-")[0]
        total = Metric.get_total_per_category(category)
        prevalence_rate = round(sum / total, 2)
        prevalence_rate = prevalence_rate * 100
        prevalence_rate = str(prevalence_rate) + "%"

        return {
            'status': status,
            'sum': sum,
            'total': total,
            'prevalence': prevalence_rate
        }

    @staticmethod
    def get_micronutrient_dashboard():

        months = [x.month for x in ChildCare.objects.dates('fhsis__date', 'month')]
        year = datetime.now().year
        latest_months = months[-3:]

        data = []
        another_list = []

        fields = datapoints.micronutrient

        mn_fields = [str(f).split(".")[2] for f in ChildCare._meta.get_fields()
                     if f.verbose_name in fields]

        for i, f in enumerate(mn_fields):

            another_list.append({
                'name': fields[i],
                'data': []
            })

            for m in latest_months:
                value = ChildCare.objects.filter(fhsis__date__month=m,
                                                     fhsis__date__year=year).aggregate(sum=Sum(f))['sum'] or 0
                data.append({
                    'month': m,
                    'field': fields[i],
                    'value': int(value)
                })

                another_list[i]['data'].append(int(value))

        final_dict = {
            'months': [general.month_converter(n) for n in latest_months],
            'values': another_list
        }

        return final_dict

    @staticmethod
    def get_maternal_dashboard():

        maternal_fields = datapoints.maternal
        fields = [maternal_fields[0], maternal_fields[4], maternal_fields[5]]

        x = [metric.to_dict() for metric in Metric.objects.filter(is_default=True) if metric.get_data_point in fields]

        values = [m['value'] for m in x]

        return {
            'fields': fields,
            'values': values
        }

    @staticmethod
    def get_child_care_dashboard():

        cc_fields = revised_datapoints.ILLNESSES

        x = [metric.to_dict() for metric in Metric.objects.all() if metric.get_data_point in cc_fields]

        values = [m['value'] for m in x]

        return {
            'fields': cc_fields,
            'values': values
        }

    # # # # # # # # # # # # # # # # NEW HERE # # # # # # # # # # #
    def get_value_over_time(self):

        point = self.get_data_point.strip()

        # hard coded
        if point == revised_datapoints.SOCIOECONOMIC[0]: point = 'Well'
        elif point == revised_datapoints.SOCIOECONOMIC[1]: point = 'Open Pit'
        elif point == revised_datapoints.SOCIOECONOMIC[2]: point = 'None'
        elif point == revised_datapoints.SOCIOECONOMIC[3]: point = 'Elementary Undergraduate'
        elif point == revised_datapoints.SOCIOECONOMIC[4]: point = 'Number of families practicing family planning'
        elif point == revised_datapoints.SOCIOECONOMIC[5]: point = 'Number of families using iodized salt'

        if self.get_source.strip() == 'InformalSettlers':

            # compute informal settlers
            a = InformalSettlers.objects.dates('date', 'year')
            year_start = a[0].year

            values = {}
            while year_start < year_now:
                total = InformalSettlers.objects.filter(date__year=year_start).aggregate(
                    sum=Sum('families_count'))['sum']
                values[year_start] = int(total)

                year_start += 1

            return json.dumps(values)

        if self.get_source.strip() == 'Family Profile':

            if point in datapoints.water_sources:
                start_year = [d.year for d in FamilyProfileLine.objects.dates('family_profile__date', 'year')][0]

                data = {}
                while start_year < weights.year_now:

                    count = FamilyProfileLine.objects.filter(family_profile__date__year=start_year, water_sources=point).count()

                    data[start_year] = count
                    start_year = start_year + 1

                return json.dumps(data)

            if point in datapoints.food_production:
                start_year = [d.year for d in FamilyProfileLine.objects.dates('family_profile__date', 'year')][0]

                data = {}
                while start_year < weights.year_now:

                    count = FamilyProfileLine.objects.filter(family_profile__date__year=start_year, food_production_activity=point).count()


                    data[start_year] = count
                    start_year = start_year + 1

                return json.dumps(data)

            if point in datapoints.educational_attainment_for_r:
                start_year = [d.year for d in FamilyProfileLine.objects.dates('family_profile__date', 'year')][0]

                data = {}
                while start_year < weights.year_now:

                    count = FamilyProfileLine.objects.filter(family_profile__date__year=start_year, educational_attainment=point).count()

                    data[start_year] = count
                    start_year = start_year + 1

                return json.dumps(data)

            if point in datapoints.toilet_type:
                start_year = [d.year for d in FamilyProfileLine.objects.dates('family_profile__date', 'year')][0]

                data = {}
                while start_year < weights.year_now:

                    count = FamilyProfileLine.objects.filter(family_profile__date__year=start_year, toilet_type=point).count()

                    data[start_year] = count
                    start_year = start_year + 1

                return json.dumps(data)

            field = consolidators.get_field(FamilyProfileLine, self.get_data_point.strip())
            start_year = [d.year for d in FamilyProfileLine.objects.dates('family_profile__date', 'year')][0]

            data = {}
            while start_year < weights.year_now:

                count = 0
                for f in FamilyProfileLine.objects.filter(family_profile__date__year=start_year):
                    if getattr(f, field):
                        count = count + 1

                data[start_year] = count
                start_year = start_year + 1

            return json.dumps(data)

        elif self.get_source.strip() == 'Maternal Care':

            field = consolidators.get_field(MaternalCare, self.get_data_point.strip())
            start_year = [d.year for d in MaternalCare.objects.all().dates('fhsis__date', 'year')][0]

            data = {}
            while start_year < weights.year_now:
                data[start_year] = float(MaternalCare.objects.filter(fhsis__date__year=start_year).aggregate(sum=Sum(field))['sum'])
                start_year += 1

            return json.dumps(data)

        elif self.get_source.strip() == 'Child Care':

            field = consolidators.get_field(ChildCare, self.get_data_point.strip())
            start_year = [d.year for d in
                           ChildCare.objects.all().dates('fhsis__date', 'year')][0]

            data = {}
            while start_year < weights.year_now:
                data[start_year] = float(ChildCare.objects.filter(fhsis__date__year=start_year).aggregate(
                    sum=Sum(field))['sum'])
                start_year += 1

            return json.dumps(data)

        elif self.get_source.strip() == 'Malaria':

            field = consolidators.get_field(Malaria, self.get_data_point.strip())
            start_year = [d.year for d in
                           Malaria.objects.all().dates('fhsis__date', 'year')][0]

            data = {}
            while start_year < weights.year_now:
                data[start_year] = float(Malaria.objects.filter(fhsis__date__year=start_year).aggregate(
                    sum=Sum(field))['sum'])
                start_year += 1

            return json.dumps(data)

        elif self.get_source.strip() == 'Immunization':

            field = consolidators.get_field(Immunization, self.get_data_point.strip())
            start_year = [d.year for d in
                           Immunization.objects.all().dates('fhsis__date', 'year')][0]

            data = {}
            while start_year < weights.year_now:
                data[start_year] = float(Immunization.objects.filter(fhsis__date__year=start_year).aggregate(
                    sum=Sum(field))['sum'])
                start_year += 1

            return json.dumps(data)

        elif self.get_source.strip() == 'Tuberculosis':

            field = consolidators.get_field(Tuberculosis, self.get_data_point.strip())
            start_year = [d.year for d in
                           Tuberculosis.objects.all().dates('fhsis__date', 'year')][0]

            data = {}
            while start_year < weights.year_now:
                data[start_year] = float(Tuberculosis.objects.filter(fhsis__date__year=start_year).aggregate(
                    sum=Sum(field))['sum'])
                start_year += 1

            return json.dumps(data)


