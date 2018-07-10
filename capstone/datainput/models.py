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
        return self.name + " | " + self.sex.name + " | " + str(self.id)


class NutritionalStatus(models.Model):

    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name + " " + str(self.id)

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

        patients = Patient.objects.filter(barangay=self)

        if patients.count() == 0:
            return False

        for patient in patients:

            try:
                mr = MonthlyReweighing.objects.get(patient=patient, date__month=datetime.now().month)
                print(mr)
            except MonthlyReweighing.DoesNotExist:
                return False

        return True


    def __str__(self):
        return str(self.id) + " " + self.name

    @property
    def has_fhsis(self):

        return FHSIS.objects.filter(barangay=self, date__month=datetime.now().month, date__year=datetime.now().year).count() > 0


class OperationTimbang(models.Model):

    date = models.DateTimeField(default=datetime.now)
    barangay = models.ForeignKey(Barangay, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey('core.Profile', on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.id) + " at " + self.barangay.name


class OPTValues(models.Model):

    opt = models.ForeignKey(OperationTimbang, on_delete=models.CASCADE)
    values = models.DecimalField(decimal_places=0, max_digits=7)
    nutritional_status = models.ForeignKey(NutritionalStatus, on_delete=models.DO_NOTHING) # 0 to 12
    age_group = models.ForeignKey(AgeGroup, on_delete=models.DO_NOTHING) # 0 to 13

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
    uploaded_by = models.ForeignKey('core.Profile', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.barangay.name + " " + str(self.date)


class FamilyProfileLine(models.Model):

    family_profile = models.ForeignKey(FamilyProfile, on_delete=models.CASCADE)
    household_no = models.CharField(max_length=20, unique=True)
    no_members = models.DecimalField(max_digits=5, decimal_places=0)
    count_05 = models.DecimalField(default=0, max_digits=5, decimal_places=0, verbose_name='Number of Children 0 - 5 months old')
    count_623 = models.DecimalField(default=0, max_digits=5, decimal_places=0, verbose_name='Number of Children 6 - 23 months old')
    count_2459 = models.DecimalField(default=0, max_digits=5, decimal_places=0, verbose_name='Number of Children 24 - 59 months old')
    count_60 = models.DecimalField(default=0, max_digits=5, decimal_places=0, verbose_name='Number of Children over 60 months old')
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
    is_family_planning = models.BooleanField(verbose_name='Is Practicing Family Planning')
    is_ebf = models.BooleanField(verbose_name='Is Practicing Exclusive Breastfeeding')
    is_mixed_milk_feeding = models.BooleanField(verbose_name='Is Practicing Mixed Milk Feeding')
    is_bottle_feeding = models.BooleanField(verbose_name='Is Practicing Bottled Feeding')

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
    is_using_iodized_salt = models.BooleanField(verbose_name='Is Using Iodized Salt')
    is_using_ifr = models.BooleanField(verbose_name='Is Using Iron Fortification')

    def __str__(self):
        return self.household_head_name + " - " + self.family_profile.barangay.name


class Patient(models.Model):

    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    barangay = models.ForeignKey(Barangay, on_delete=models.CASCADE)
    sex = models.ForeignKey(Sex, on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(default=datetime.now)

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
    uploaded_by = models.ForeignKey('core.Profile', on_delete=models.DO_NOTHING)

    def __str__(self):
        return '%s - %s' % (self.patient.barangay.name, str(self.date.month))

    def get_nutritional_status(self):

        statuses = [
            'Height for Age - ' + str(self.height_for_age),
            'Weight for Age - ' + str(self.weight_for_age),
            'Weight for Height/Length - ' + str(self.weight_for_height_length)
        ]

        return statuses


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

    families_count = models.DecimalField(max_digits=5, decimal_places=0, verbose_name='Number of Families')
    date = models.DateField(default=datetime.now)

    def __str__(self):
        return "Informal Settlers - " + str(self.date.month) + str(self.date.year)


class FHSIS(models.Model):

    date = models.DateTimeField(default=datetime.now)
    uploaded_by = models.ForeignKey('core.Profile', on_delete=models.DO_NOTHING)
    barangay = models.ForeignKey(Barangay, on_delete=models.CASCADE)

    def __str__(self):
        return "FHSIS for " + str(self.date) + " - " + self.barangay.name


class MaternalCare(models.Model):

    prenatal_visits = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Pregnant women with 4 or more prenatal visits')
    tetanus_toxoid = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Pregnant women given 2 doses of Tetanus Toxoid')
    tt2_plus = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Pregnant women given TT2 plus')
    complete_iron = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Pregnant women given complete iron with folic acid supplementation')
    complete_iron_post = models.DecimalField(max_digits=5, decimal_places=2,
                                        verbose_name='Postpartum women with given complete iron supplementation')
    postpartum_visits = models.DecimalField(max_digits=5, decimal_places=2,
                                        verbose_name='Postpartum women with at least 2 postpartum visits')
    vitamin_a = models.DecimalField(max_digits=5, decimal_places=2,
                                        verbose_name='Postpartum women given Vitamin A supplementation')
    breastfed = models.DecimalField(max_digits=5, decimal_places=2,
                                        verbose_name='Postpartum women initiated breastfeeding within 1 hour after delivery')
    deliveries = models.DecimalField(max_digits=5, decimal_places=2)

    fhsis = models.ForeignKey(FHSIS, on_delete=models.CASCADE)


class Immunization(models.Model):

    immunization_given = models.DecimalField(decimal_places=2, max_digits=5)
    fully_immunized_child = models.DecimalField(decimal_places=2, max_digits=5)
    child_protected_at_birth = models.DecimalField(decimal_places=2, max_digits=5)

    given_bcg = models.IntegerField()
    given_hepa = models.IntegerField()
    given_penta = models.IntegerField()
    given_opv = models.IntegerField()
    given_mcv = models.IntegerField()
    given_rota = models.IntegerField()
    given_pcv = models.IntegerField()

    fhsis = models.ForeignKey(FHSIS, on_delete=models.CASCADE)
    sex = models.ForeignKey(Sex, on_delete=models.CASCADE)


class Malaria(models.Model):

    population_at_risk = models.DecimalField(decimal_places=2, max_digits=5)
    malaria_cases = models.DecimalField(decimal_places=2, max_digits=5)
    deaths = models.DecimalField(decimal_places=2, max_digits=5)
    immunization_given = models.DecimalField(decimal_places=2, max_digits=5)
    llin_given = models.DecimalField(decimal_places=2, max_digits=5)

    fhsis = models.ForeignKey(FHSIS, on_delete=models.CASCADE)
    sex = models.ForeignKey(Sex, on_delete=models.CASCADE)


class Tuberculosis(models.Model):

    underwent_ddsm = models.DecimalField(decimal_places=2, max_digits=5)
    smear_positive = models.DecimalField(decimal_places=2, max_digits=5)
    cases_cured = models.DecimalField(decimal_places=2, max_digits=5)
    identified = models.DecimalField(decimal_places=2, max_digits=5)

    fhsis = models.ForeignKey(FHSIS, on_delete=models.CASCADE)
    sex = models.ForeignKey(Sex, on_delete=models.CASCADE)


class Schistosomiasis(models.Model):

    cases_cured = models.DecimalField(decimal_places=2, max_digits=5)
    cases = models.DecimalField(decimal_places=2, max_digits=5)

    fhsis = models.ForeignKey(FHSIS, on_delete=models.CASCADE)
    sex = models.ForeignKey(Sex, on_delete=models.CASCADE)


class Flariasis(models.Model):

    cases = models.DecimalField(decimal_places=2, max_digits=5)
    mfd = models.DecimalField(decimal_places=2, max_digits=5)
    given_MDA = models.DecimalField(decimal_places=2, max_digits=5)

    fhsis = models.ForeignKey(FHSIS, on_delete=models.CASCADE)
    sex = models.ForeignKey(Sex, on_delete=models.CASCADE)


class Leprosy(models.Model):

    cases = models.DecimalField(decimal_places=2, max_digits=5)
    cases_cured = models.DecimalField(decimal_places=2, max_digits=5)

    fhsis = models.ForeignKey(FHSIS, on_delete=models.CASCADE)
    sex = models.ForeignKey(Sex, on_delete=models.CASCADE)


class ChildCare(models.Model):

    given_complimentary_food = models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Given complimentary food')
    received_vitamin_A = models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Infants who received vitamin A')
    received_iron = models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Infants who received iron')
    received_MNP = models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Infants who received MNP')
    sick_children = models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Sick children')
    given_deworming = models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Children given deworming')
    anemic_children = models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Anemic children')
    anemic_children_with_iron = models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Anemic children receiving full dose iron')
    diarrhea_cases = models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Diarrhea cases')
    diarrhea_with_ORS = models.DecimalField(decimal_places=2, max_digits=5)
    pneumonia_cases = models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Pneumonia cases')
    pneumonia_cases_with_Tx = models.DecimalField(decimal_places=2, max_digits=5)

    fhsis = models.ForeignKey(FHSIS, on_delete=models.CASCADE)
    sex = models.ForeignKey(Sex, on_delete=models.CASCADE)


class STISurveillance(models.Model):

    fhsis = models.ForeignKey(FHSIS, on_delete=models.CASCADE)
    number_of_pregnant_women_seen = models.DecimalField(decimal_places=2, max_digits=5)
    number_of_pregnant_women_with_Syphilis = models.DecimalField(decimal_places=2, max_digits=5)
    number_of_pregnant_women_given_Penicillin = models.DecimalField(decimal_places=2, max_digits=5)

