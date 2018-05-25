from datetime import datetime
from django.db import models


class AgeGroup(models.Model):

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    SEX_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)

    def __str__(self):
        return self.name + " | " + self.sex


class NutritionalStatus(models.Model):

    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "nutritional statuses"


class Barangay(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class OperationTimbang(models.Model):

    date = models.DateTimeField(default=datetime.now)
    barangay = models.ForeignKey(Barangay, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=50)

    def __str__(self):
        return str(self.date) + " at " + self.barangay.name


class OPTValues(models.Model):
    opt = models.ForeignKey(OperationTimbang, on_delete=models.CASCADE)
    values = models.DecimalField(decimal_places=0, max_digits=7)
    nutritional_status = models.ForeignKey(NutritionalStatus, on_delete=models.DO_NOTHING)
    age_group = models.ForeignKey(AgeGroup, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name_plural = 'OPT Values'

    def __str__(self):
        return self.nutritional_status.name + " " + self.age_group.name
