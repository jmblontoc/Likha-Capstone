from django.db import models

# Create your models here.

class CorrelationConf(models.Model):

    script = models.TextField()
    report = models.CharField(max_length=50, default='micro')

    def __str__(self):
        return self.report