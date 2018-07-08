import decimal
from datetime import datetime
from friends import datapoints
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