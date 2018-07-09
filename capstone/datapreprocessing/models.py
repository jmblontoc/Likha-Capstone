import decimal
from datetime import datetime

from django.db.models import Sum

from datainput.models import ChildCare
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

    def __str__(self):
        return self.metric

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

        return [x for x in Metric.objects.all() if x.get_total_value >= x.threshold]


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
                                                     fhsis__date__year=year).aggregate(sum=Sum(f))['sum']
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


