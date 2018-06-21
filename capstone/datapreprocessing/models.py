import decimal
from datetime import datetime
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


class RootCause(models.Model):

    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class DataMap(models.Model):

    root_cause = models.ForeignKey(RootCause, on_delete=models.CASCADE)
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.root_cause} - {self.metric.metric}"



