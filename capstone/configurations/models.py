from django.db import models

# Create your models here.


class CorrelationConf(models.Model):

    script = models.TextField()
    report = models.CharField(max_length=50, default='micro')

    def __str__(self):
        return self.report


class NotifyBNS(models.Model):

    days_before = models.PositiveIntegerField()

    def __str__(self):
        return "%i days" % self.days_before
