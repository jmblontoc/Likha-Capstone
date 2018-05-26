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


class FamilyProfile(models.Model):

    barangay = models.ForeignKey(Barangay, on_delete=models.CASCADE)
    household_no = models.CharField(max_length=20)
    no_members = models.DecimalField(max_digits=5, decimal_places=0)
    count_05 = models.DecimalField(max_digits=5, decimal_places=0, verbose_name='Number of Children 0 - 5 months old')
    count_623 = models.DecimalField(max_digits=5, decimal_places=0, verbose_name='Number of Children 6 - 23 months old')
    count_2459 = models.DecimalField(max_digits=5, decimal_places=0, verbose_name='Number of Children 24 - 59 months old')
    count_60 = models.DecimalField(max_digits=5, decimal_places=0, verbose_name='Number of Children over 60 months old')
    household_head_name = models.CharField(max_length=100)
    occupation = models.CharField(max_length=50)
    educational_attainment = models.CharField(max_length=50)
    is_mother_pregnant = models.BooleanField()
    is_family_planning = models.BooleanField()
    is_ebf = models.BooleanField()
    is_mixed_milk_feeding = models.BooleanField()
    is_bottle_feeding = models.BooleanField()

    TOILET_TYPES = (
        ('WS', 'WS'),
        ('OP', 'OP'),
        ('O', 'O'),
        ('N', 'N')
    )

    WATER_SOURCES = (
        ('P', 'P'),
        ('W', 'W'),
        ('S', 'S')
    )

    FOOD_PRODUCTION_ACTIVITIES = (
        ('VG', 'VG'),
        ('PL', 'PL'),
        ('FP', 'FP')
    )

    toilet_type = models.CharField(max_length=10, choices=TOILET_TYPES)
    water_sources = models.CharField(max_length=10, choices=WATER_SOURCES)
    food_production_activity = models.CharField(max_length=10, choices=FOOD_PRODUCTION_ACTIVITIES)
    is_using_iodized_salt = models.BooleanField()
    is_using_ifr = models.BooleanField()

    def __str__(self):
        return self.household_head_name + " - " + self.barangay.name

