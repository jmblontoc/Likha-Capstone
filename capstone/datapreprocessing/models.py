from datetime import datetime

from django.db import models

# Create your models here.


class DataMap(models.Model):

    metric = models.CharField(max_length=150)
    threshold = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=datetime.now)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.metric
