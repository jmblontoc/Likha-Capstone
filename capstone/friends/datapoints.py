
# family profile
from datainput.models import ChildCare, Tuberculosis

educational_attainment = [
    'Elementary Undergraduate',
    'Elementary Graduate',
    'Highschool Undergraduate',
    'Highschool Graduate',
    'College Undergraduate',
    'College Graduate',
    'Vocational',
    'Others'
]

educational_attainment_for_r = [
    'Elementary Undergraduate',
    'Highschool Undergraduate',
    'College Undergraduate',
    'Vocational',
]

toilet_type = [
    'Water Sealed',
    'Open Pit',
    'Others',
    'None'
]

water_sources = [
    'Pipe',
    'Well',
    'Spring'
]

food_production = [
    'Fishpond',
    'Poultry/Livestock',
    'Vegetable Garden'
]

main_family_profile = [
    'no_members',
    'count_05',
    'count_623',
    'count_2459',
    'count_60'
]

boolean_fields_fp = [
    'is_mother_pregnant',
    'is_family_planning',
    'is_ebf',
    'is_mixed_milk_feeding',
    'is_bottle_feeding',
    'is_using_iodized_salt',
    'is_using_ifr'
]

micronutrient = [
    'Number of children who received vitamin A',
    'Number of children who received iron',
    'Number of children who received MNP'
]

maternal = [
    'Number of Pregnant women with 4 or more prenatal visits',
    'Number of Pregnant women given 2 doses of Tetanus Toxoid',
    'Number of Postpartum women with at least 2 postpartum visits',
    'Number of Pregnant women given TT2 plus',
    'Number of Pregnant women given complete iron with folic acid supplementation',
    'Number of Postpartum women with given complete iron supplementation',
    'Number of Postpartum women given Vitamin A supplementation'
]

child_care = [
    'Given complimentary food',
    'Number of Sick children',
    'Children given deworming',
    'Number of Anemic children',
    'Number of Anemic children receiving full dose iron',
    'Number of Diarrhea cases',
    'Number of Pneumonia cases'
]

immunizations = [
    'Number of Children Given BCG',
    'Number of Children Given HEPA',
    'Number of Children Given PENTA',
    'Number of Children Given OPV',
    'Number of Children Given MCV',
    'Number of Children Given ROTA',
    'Number of Children Given PCV',
]

malaria = [
    'Number of Malaria Cases',
    'Malaria Deaths',
    'Malaria Immunization Given'
]

tuberculosis = [
    'Number of Tuberculosis Identified'
]

socioeconomic = [
    'Is Practicing Family Planning',
    'Is Practicing Exclusive Breastfeeding',
    'Is Practicing Mixed Milk Feeding',
    'Is Practicing Bottled Feeding',
    'Is Using Iodized Salt',
    'Is Using Iron Fortification',


    'Fishpond',
    'Poultry/Livestock',
    'Vegetable Garden',

    'Pipe',
    'Well',
    'Spring',
    'Water Sealed',
    'Open Pit',

    'Elementary Undergraduate',
    'Elementary Graduate',
    'Highschool Undergraduate',
    'Highschool Graduate',
    'College Undergraduate',
    'College Graduate',
    'Vocational'
]

# # # # # # # # #

# # # # # # DEPRECATED!!! # # # # #


# Child Care
def get_child_care_fields():
    # 113

    return ChildCare._meta.get_fields()[1:13]


# Tuberculosis
def get_tb_fields():

    return Tuberculosis._meta.get_fields()[1:5]


# Malaria
def get_malaria_fields():

    pass