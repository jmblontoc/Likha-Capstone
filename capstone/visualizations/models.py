from datetime import datetime

from django.db import models

# Create your models here.


class Report(models.Model):

    name = models.CharField(max_length=128)
    date = models.DateTimeField(default=datetime.now)
    json_data = models.TextField()

    comments = models.TextField()
    generated_by = models.ForeignKey('core.Profile', on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.name, str(self.date.date()))

    def to_dict(self):
        return eval(self.json_data)
