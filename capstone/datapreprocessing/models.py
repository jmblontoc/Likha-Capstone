import decimal
import json
from datetime import datetime

from django.db.models import Sum

from computations import weights
from datainput.models import ChildCare, FamilyProfileLine, MaternalCare, Malaria, Immunization, Tuberculosis
from friends import datapoints, general
from friends.datapreprocessing import consolidators
from django.db import models

# Create your models here.


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

        cc_fields = datapoints.child_care
        fields = [cc_fields[1], cc_fields[3], cc_fields[5], cc_fields[6]]

        x = [metric.to_dict() for metric in Metric.objects.filter(is_default=True) if metric.get_data_point in fields]

        values = [m['value'] for m in x]

        return {
            'fields': fields,
            'values': values
        }


    # # # # # # # # # # # # # # # # NEW HERE # # # # # # # # # # #

    def get_value_over_time(self):

        point = self.get_data_point.strip()

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
            start_month = [d.month for d in MaternalCare.objects.filter(fhsis__date__year=weights.year_now).dates('fhsis__date', 'month')][0]

            data = {}
            while start_month <= weights.month_now:
                data[general.month_converter(start_month)] = float(MaternalCare.objects.filter(fhsis__date__year=weights.year_now, fhsis__date__month=start_month).aggregate(sum=Sum(field))['sum'])
                start_month = start_month + 1

            return json.dumps(data)

        elif self.get_source.strip() == 'Child Care':

            field = consolidators.get_field(ChildCare, self.get_data_point.strip())
            start_month = [d.month for d in
                           ChildCare.objects.filter(fhsis__date__year=weights.year_now).dates('fhsis__date',
                                                                                                 'month')][0]

            data = {}
            while start_month <= weights.month_now:
                data[general.month_converter(start_month)] = float(ChildCare.objects.filter(fhsis__date__year=weights.year_now,
                                                                      fhsis__date__month=start_month).aggregate(
                    sum=Sum(field))['sum'])
                start_month = start_month + 1

            return json.dumps(data)

        elif self.get_source.strip() == 'Malaria':

            field = consolidators.get_field(Malaria, self.get_data_point.strip())
            start_month = [d.month for d in
                           Malaria.objects.filter(fhsis__date__year=weights.year_now).dates('fhsis__date',
                                                                                                 'month')][0]

            data = {}
            while start_month <= weights.month_now:
                data[general.month_converter(start_month)] = float(Malaria.objects.filter(fhsis__date__year=weights.year_now,
                                                                      fhsis__date__month=start_month).aggregate(
                    sum=Sum(field))['sum'])
                start_month = start_month + 1

            return json.dumps(data)

        elif self.get_source.strip() == 'Immunization':

            field = consolidators.get_field(Immunization, self.get_data_point.strip())
            start_month = [d.month for d in
                           Immunization.objects.filter(fhsis__date__year=weights.year_now).dates('fhsis__date',
                                                                                                 'month')][0]

            data = {}
            while start_month <= weights.month_now:
                data[general.month_converter(start_month)] = float(Immunization.objects.filter(fhsis__date__year=weights.year_now,
                                                                      fhsis__date__month=start_month).aggregate(
                    sum=Sum(field))['sum'])
                start_month = start_month + 1

            return json.dumps(data)

        elif self.get_source.strip() == 'Tuberculosis':

            field = consolidators.get_field(Tuberculosis, self.get_data_point.strip())
            start_month = [d.month for d in
                           Tuberculosis.objects.filter(fhsis__date__year=weights.year_now).dates('fhsis__date',
                                                                                                 'month')][0]

            data = {}
            while start_month <= weights.month_now:
                data[general.month_converter(start_month)] = float(Tuberculosis.objects.filter(fhsis__date__year=weights.year_now,
                                                                      fhsis__date__month=start_month).aggregate(
                    sum=Sum(field))['sum'])
                start_month = start_month + 1

            return json.dumps(data)


