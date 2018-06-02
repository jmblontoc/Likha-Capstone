

from datetime import datetime
from django.db import models
import datetime as dt


class Sex(models.Model):

    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class AgeGroup(models.Model):

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    sex = models.ForeignKey(Sex, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " | " + self.sex.name


class NutritionalStatus(models.Model):

    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "nutritional statuses"


class Barangay(models.Model):

    name = models.CharField(max_length=100)

    @property
    def has_family_profile(self):
        return FamilyProfile.objects.filter(barangay=self, date__year=datetime.now().year).count() > 0

    @property
    def has_opt(self):
        return OperationTimbang.objects.filter(barangay=self, date__year=datetime.now().year).count() > 0

    @property
    def has_reweighed(self):
        return MonthlyReweighing.objects.filter(patient__barangay=self, date__month=datetime.now().month).count() > 0


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


class WeightForAge(models.Model):

    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class HeightForAge(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class WeightForHeightLength(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class FamilyProfile(models.Model):

    barangay = models.ForeignKey(Barangay, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.barangay.name + " " + str(self.date)


class FamilyProfileLine(models.Model):

    family_profile = models.ForeignKey(FamilyProfile, on_delete=models.CASCADE)
    household_no = models.CharField(max_length=20, unique=True)
    no_members = models.DecimalField(max_digits=5, decimal_places=0)
    count_05 = models.DecimalField(max_digits=5, decimal_places=0, verbose_name='Number of Children 0 - 5 months old')
    count_623 = models.DecimalField(max_digits=5, decimal_places=0, verbose_name='Number of Children 6 - 23 months old')
    count_2459 = models.DecimalField(max_digits=5, decimal_places=0, verbose_name='Number of Children 24 - 59 months old')
    count_60 = models.DecimalField(max_digits=5, decimal_places=0, verbose_name='Number of Children over 60 months old')
    household_head_name = models.CharField(max_length=100)
    occupation = models.CharField(max_length=50)

    EDUCATIONAL_ATTAINMENT = (
        ('Elementary Undergraduate', 'Elementary Undergraduate'),
        ('Elementary Graduate', 'Elementary Graduate'),
        ('Highschool Undergraduate', 'Highschool Undergraduate'),
        ('Highschool Graduate', 'Highschool Graduate'),
        ('College Undergraduate', 'College Undergraduate'),
        ('College Graduate', 'College Graduate'),
        ('Vocational', 'Vocational'),
        ('Others', 'Others')
    )

    educational_attainment = models.CharField(max_length=50, choices=EDUCATIONAL_ATTAINMENT)
    is_mother_pregnant = models.BooleanField()
    is_family_planning = models.BooleanField()
    is_ebf = models.BooleanField()
    is_mixed_milk_feeding = models.BooleanField()
    is_bottle_feeding = models.BooleanField()

    TOILET_TYPES = (
        ('Water Sealed', 'Water Sealed'),
        ('Open Pit', 'Open Pit'),
        ('Others', 'Others'),
        ('None', 'None')
    )

    WATER_SOURCES = (
        ('Pipe', 'Pipe'),
        ('Well', 'Well'),
        ('Spring', 'Spring')
    )

    FOOD_PRODUCTION_ACTIVITIES = (
        ('Vegetable Garden', 'Vegetable Garden'),
        ('Poultry/Livestock', 'Poultry/Livestock'),
        ('Fishpond', 'Fishpond')
    )

    toilet_type = models.CharField(max_length=50, choices=TOILET_TYPES)
    water_sources = models.CharField(max_length=50, choices=WATER_SOURCES)
    food_production_activity = models.CharField(max_length=50, choices=FOOD_PRODUCTION_ACTIVITIES)
    is_using_iodized_salt = models.BooleanField()
    is_using_ifr = models.BooleanField()

    def __str__(self):
        return self.household_head_name + " - " + self.family_profile.barangay.name


class Patient(models.Model):

    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    barangay = models.ForeignKey(Barangay, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " - " + self.barangay.name

    @property
    def get_age(self):
        months =  (dt.datetime.now().date() - self.date_of_birth)
        age_months = months.days / 12
        return int(age_months)

    @property
    def get_reweighing_status(self):

        try:
            x = MonthlyReweighing.objects.get(patient__name=self.name, date__month=datetime.now().month)
        except MonthlyReweighing.DoesNotExist:
            return 'Not yet updated'

        return 'Updated'


class MonthlyReweighing(models.Model):

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    weight_for_age = models.ForeignKey(WeightForAge, on_delete=models.CASCADE)
    height_for_age = models.ForeignKey(HeightForAge, on_delete=models.CASCADE)
    weight_for_height_length = models.ForeignKey(WeightForHeightLength, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now)
    status = models.CharField(max_length=40)

    def __str__(self):
        return self.patient.name


class HealthCareWasteManagement(models.Model):

    date = models.DateField(default=datetime.now)
    with_syringe = models.DecimalField(decimal_places=0, verbose_name='Health Centers With Syringe Collection', max_digits=5)
    with_safe_water = models.DecimalField(decimal_places=0, max_digits=5, verbose_name='Households With Access to Improved or Safe Water')
    with_sanitary_toilet = models.DecimalField(decimal_places=0, max_digits=5, verbose_name='Households With Sanitary Toilet')
    with_satisfactoral_disposal = models.DecimalField(decimal_places=0, max_digits=5, verbose_name='Households With Satisfactoral Disposal of Solid Waste')
    with_complete_facilities = models.DecimalField(decimal_places=0, max_digits=5, verbose_name='Household With Complete Basic Sanitation Facilities')

    def __str__(self):
        return "HCWM - " + str(self.date)


class UnemploymentRate(models.Model):

    date = models.DateField(default=datetime.now)
    rate = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self):
        return "Rate - " + str(self.date.year)


class InformalSettlers(models.Model):

    families_count = models.DecimalField(max_digits=5, decimal_places=0)
    date = models.DateField(default=datetime.now)

    def __str__(self):
        return "Informal Settlers - " + str(self.date.year)


