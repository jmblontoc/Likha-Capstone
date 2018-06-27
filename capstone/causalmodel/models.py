from django.db import models

# Create your models here.


class RootCause(models.Model):

    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class DataMap(models.Model):

    root_cause = models.ForeignKey(RootCause, on_delete=models.CASCADE)
    metric = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    threshold = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return '%s - %s' % (self.root_cause.name, self.metric)
