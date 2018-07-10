from computations import weights, child_care, maternal, socioeconomic
from datainput.models import *
from friends.datamining import correlations as c
from friends import datapoints

records = weights.weights_per_year_to_dict()

def display_micronutrient(scores):

    fields = [f for f in ChildCare._meta.get_fields() if f.verbose_name in datapoints.micronutrient]

    for f in fields:
        point = str(f).strip().split(".")[2]
        data_point = child_care.get_fhsis(ChildCare, point, None)
        score = c.get_correlation_score(c.make_variables(records[0], data_point))

        scores.append(
            {
                'category': 'Weight for Age - Underweight and Severely Underweight',
                'source': 'Child Care',
                'field': f.verbose_name,
                'score': score,
                'report': 'Micronutrient Supplementation',
                'variables': c.make_variables(records[0], data_point)
            }
        )

    for f in fields:
        point = str(f).strip().split(".")[2]
        data_point = child_care.get_fhsis(ChildCare, point, None)
        score = c.get_correlation_score(c.make_variables(records[1], data_point))

        scores.append(
            {
                'category': 'Height for Age - Stunted and Severely Stunted',
                'source': 'Child Care',
                'field': f.verbose_name,
                'score': score,
                'report': 'Micronutrient Supplementation',
                'variables': c.make_variables(records[1], data_point)
            }
        )

    for f in fields:
        point = str(f).strip().split(".")[2]
        data_point = child_care.get_fhsis(ChildCare, point, None)
        score = c.get_correlation_score(c.make_variables(records[2], data_point))

        scores.append(
            {
                'category': 'Weight for Height/Length - Wasted and Severely Wasted',
                'source': 'Child Care',
                'field': f.verbose_name,
                'score': score,
                'report': 'Micronutrient Supplementation',
                'variables': c.make_variables(records[2], data_point)
            }
        )


def display_maternal(scores):

    fields = [f for f in MaternalCare._meta.get_fields() if f.verbose_name in datapoints.maternal]

    for f in fields:
        point = str(f).strip().split(".")[2]
        data_point = maternal.get_maternal_care(point)
        score = c.get_correlation_score(c.make_variables(records[0], data_point))

        scores.append(
            {
                'category': 'Weight for Age - Underweight and Severely Underweight',
                'source': 'Maternal Care',
                'field': f.verbose_name,
                'score': score,
                'report': 'City Maternal Care',
                'variables': c.make_variables(records[0], data_point)
            }
        )

    for f in fields:
        point = str(f).strip().split(".")[2]
        data_point = maternal.get_maternal_care(point)
        score = c.get_correlation_score(c.make_variables(records[1], data_point))

        scores.append(
            {
                'category': 'Height for Age - Stunted and Severely Stunted',
                'source': 'Maternal Care',
                'field': f.verbose_name,
                'score': score,
                'report': 'City Maternal Care',
                'variables': c.make_variables(records[1], data_point)
            }
        )

    for f in fields:
        point = str(f).strip().split(".")[2]
        data_point = maternal.get_maternal_care(point)
        score = c.get_correlation_score(c.make_variables(records[2], data_point))

        scores.append(
            {
                'category': 'Weight for Height/Length - Wasted and Severely Wasted',
                'source': 'Maternal Care',
                'field': f.verbose_name,
                'score': score,
                'report': 'City Maternal Care',
                'variables': c.make_variables(records[2], data_point)
            }
        )


def display_child_care(scores):
    fields = [f for f in ChildCare._meta.get_fields() if f.verbose_name in datapoints.child_care]

    for f in fields:
        point = str(f).strip().split(".")[2]
        data_point = child_care.get_fhsis(ChildCare, point, None)
        score = c.get_correlation_score(c.make_variables(records[0], data_point))

        scores.append(
            {
                'category': 'Weight for Age - Underweight and Severely Underweight',
                'source': 'Child Care',
                'field': f.verbose_name,
                'score': score,
                'report': 'City Children Care',
                'variables': c.make_variables(records[0], data_point)
            }
        )

    for f in fields:
        point = str(f).strip().split(".")[2]
        data_point = child_care.get_fhsis(ChildCare, point, None)
        score = c.get_correlation_score(c.make_variables(records[1], data_point))

        scores.append(
            {
                'category': 'Height for Age - Stunted and Severely Stunted',
                'source': 'Child Care',
                'field': f.verbose_name,
                'score': score,
                'report': 'City Children Care',
                'variables': c.make_variables(records[1], data_point)
            }
        )

    for f in fields:
        point = str(f).strip().split(".")[2]
        data_point = child_care.get_fhsis(ChildCare, point, None)
        score = c.get_correlation_score(c.make_variables(records[2], data_point))

        scores.append(
            {
                'category': 'Weight for Height/Length - Wasted and Severely Wasted',
                'source': 'Child Care',
                'field': f.verbose_name,
                'score': score,
                'report': 'City Children Care',
                'variables': c.make_variables(records[2], data_point)
            }
        )


def display_socioeconomic(scores):

    fields = socioeconomic.fields

    for f in fields:
        data_point = socioeconomic.get_socioeconomic(f)
        score = c.get_correlation_score(c.make_variables(records[0], data_point))

        scores.append(
            {
                'category': 'Weight for Age - Underweight and Severely Underweight',
                'source': 'Family Profile',
                'field': f,
                'score': score,
                'report': 'Socioeconomic',
                'variables': c.make_variables(records[0], data_point)
            }
        )

    for f in fields:
        data_point = socioeconomic.get_socioeconomic(f)
        score = c.get_correlation_score(c.make_variables(records[0], data_point))

        scores.append(
            {
                'category': 'Height for Age - Stunted and Severely Stunted',
                'source': 'Family Profile',
                'field': f,
                'score': score,
                'report': 'Socioeconomic',
                'variables': c.make_variables(records[1], data_point)
            }
        )

    for f in fields:
        data_point = socioeconomic.get_socioeconomic(f)
        score = c.get_correlation_score(c.make_variables(records[0], data_point))

        scores.append(
            {
                'category': 'Weight for Height/Length - Wasted and Severely Wasted',
                'source': 'Family Profile',
                'field': f,
                'score': score,
                'report': 'Socioeconomic',
                'variables': c.make_variables(records[2], data_point)
            }
        )

    return scores