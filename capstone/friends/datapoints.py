
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