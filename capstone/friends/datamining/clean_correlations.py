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
                'variables': c.make_variables(records[0], data_point),
                'remark': get_correlation_remark(score)
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
                'variables': c.make_variables(records[1], data_point),
                'remark': get_correlation_remark(score)
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
                'variables': c.make_variables(records[2], data_point),
                'remark': get_correlation_remark(score)
            }
        )

    return scores


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
                'variables': c.make_variables(records[0], data_point),
                'remark': get_correlation_remark(score)
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
                'variables': c.make_variables(records[1], data_point),
                'remark': get_correlation_remark(score)
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
                'variables': c.make_variables(records[2], data_point),
                'remark': get_correlation_remark(score)
            }
        )

    return scores


def display_child_care(scores):
    fields = [f for f in ChildCare._meta.get_fields() if f.verbose_name in datapoints.child_care]
    immunization_fields = [f for f in Immunization._meta.get_fields() if f.verbose_name in datapoints.immunizations]
    malaria_fields = [f for f in Malaria._meta.get_fields() if f.verbose_name in datapoints.malaria]
    tb_fields = [f for f in Tuberculosis._meta.get_fields() if f.verbose_name in datapoints.tuberculosis]


    # original child care
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
                'variables': c.make_variables(records[0], data_point),
                'remark': get_correlation_remark(score)
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
                'variables': c.make_variables(records[1], data_point),
                'remark': get_correlation_remark(score)
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
                'variables': c.make_variables(records[2], data_point),
                'remark': get_correlation_remark(score)
            }
        )

    # immunizations
    for f in immunization_fields:
        point = str(f).strip().split(".")[2]
        data_point = child_care.get_fhsis(Immunization, point, None)
        score = c.get_correlation_score(c.make_variables(records[0], data_point))

        scores.append(
            {
                'category': 'Weight for Age - Underweight and Severely Underweight',
                'source': 'Child Care',
                'field': f.verbose_name,
                'score': score,
                'report': 'City Children Care',
                'variables': c.make_variables(records[0], data_point),
                'remark': get_correlation_remark(score)
            }
        )

    for f in immunization_fields:
        point = str(f).strip().split(".")[2]
        data_point = child_care.get_fhsis(Immunization, point, None)
        score = c.get_correlation_score(c.make_variables(records[1], data_point))

        scores.append(
            {
                'category': 'Height for Age - Stunted and Severely Stunted',
                'source': 'Child Care',
                'field': f.verbose_name,
                'score': score,
                'report': 'City Children Care',
                'variables': c.make_variables(records[1], data_point),
                'remark': get_correlation_remark(score)
            }
        )

    for f in immunization_fields:
        point = str(f).strip().split(".")[2]
        data_point = child_care.get_fhsis(Immunization, point, None)
        score = c.get_correlation_score(c.make_variables(records[2], data_point))

        scores.append(
            {
                'category': 'Weight for Height/Length - Wasted and Severely Wasted',
                'source': 'Child Care',
                'field': f.verbose_name,
                'score': score,
                'report': 'City Children Care',
                'variables': c.make_variables(records[2], data_point),
                'remark': get_correlation_remark(score)
            }
        )

    # malaria
    for f in malaria_fields:
        point = str(f).strip().split(".")[2]
        data_point = child_care.get_fhsis(Malaria, point, None)
        score = c.get_correlation_score(c.make_variables(records[0], data_point))

        scores.append(
            {
                'category': 'Weight for Age - Underweight and Severely Underweight',
                'source': 'Child Care',
                'field': f.verbose_name,
                'score': score,
                'report': 'City Children Care',
                'variables': c.make_variables(records[0], data_point),
                'remark': get_correlation_remark(score)
            }
        )

    for f in malaria_fields:
        point = str(f).strip().split(".")[2]
        data_point = child_care.get_fhsis(Malaria, point, None)
        score = c.get_correlation_score(c.make_variables(records[1], data_point))

        scores.append(
            {
                'category': 'Height for Age - Stunted and Severely Stunted',
                'source': 'Child Care',
                'field': f.verbose_name,
                'score': score,
                'report': 'City Children Care',
                'variables': c.make_variables(records[1], data_point),
                'remark': get_correlation_remark(score)
            }
        )

    for f in malaria_fields:
        point = str(f).strip().split(".")[2]
        data_point = child_care.get_fhsis(Malaria, point, None)
        score = c.get_correlation_score(c.make_variables(records[2], data_point))

        scores.append(
            {
                'category': 'Weight for Height/Length - Wasted and Severely Wasted',
                'source': 'Child Care',
                'field': f.verbose_name,
                'score': score,
                'report': 'City Children Care',
                'variables': c.make_variables(records[2], data_point),
                'remark': get_correlation_remark(score)
            }
        )

    # tb
    for f in tb_fields:
        point = str(f).strip().split(".")[2]
        data_point = child_care.get_fhsis(Tuberculosis, point, None)
        score = c.get_correlation_score(c.make_variables(records[0], data_point))

        scores.append(
            {
                'category': 'Weight for Age - Underweight and Severely Underweight',
                'source': 'Child Care',
                'field': f.verbose_name,
                'score': score,
                'report': 'City Children Care',
                'variables': c.make_variables(records[0], data_point),
                'remark': get_correlation_remark(score)
            }
        )

    for f in tb_fields:
        point = str(f).strip().split(".")[2]
        data_point = child_care.get_fhsis(Tuberculosis, point, None)
        score = c.get_correlation_score(c.make_variables(records[1], data_point))

        scores.append(
            {
                'category': 'Height for Age - Stunted and Severely Stunted',
                'source': 'Child Care',
                'field': f.verbose_name,
                'score': score,
                'report': 'City Children Care',
                'variables': c.make_variables(records[1], data_point),
                'remark': get_correlation_remark(score)
            }
        )

    for f in tb_fields:
        point = str(f).strip().split(".")[2]
        data_point = child_care.get_fhsis(Tuberculosis, point, None)
        score = c.get_correlation_score(c.make_variables(records[2], data_point))

        scores.append(
            {
                'category': 'Weight for Height/Length - Wasted and Severely Wasted',
                'source': 'Child Care',
                'field': f.verbose_name,
                'score': score,
                'report': 'City Children Care',
                'variables': c.make_variables(records[2], data_point),
                'remark': get_correlation_remark(score)
            }
        )

    return scores


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
                'variables': c.make_variables(records[0], data_point),
                'remark': get_correlation_remark(score)
            }
        )

    for f in fields:
        data_point = socioeconomic.get_socioeconomic(f)
        score = c.get_correlation_score(c.make_variables(records[1], data_point))

        scores.append(
            {
                'category': 'Height for Age - Stunted and Severely Stunted',
                'source': 'Family Profile',
                'field': f,
                'score': score,
                'report': 'Socioeconomic',
                'variables': c.make_variables(records[1], data_point),
                'remark': get_correlation_remark(score)
            }
        )

    for f in fields:
        data_point = socioeconomic.get_socioeconomic(f)
        score = c.get_correlation_score(c.make_variables(records[2], data_point))

        scores.append(
            {
                'category': 'Weight for Height/Length - Wasted and Severely Wasted',
                'source': 'Family Profile',
                'field': f,
                'score': score,
                'report': 'Socioeconomic',
                'variables': c.make_variables(records[2], data_point),
                'remark': get_correlation_remark(score)
            }
        )

    data_point = socioeconomic.get_members_data()
    score = c.get_correlation_score(c.make_variables(records[0], data_point))

    scores.append(
        {
            'category': 'Weight for Age - Underweight and Severely Underweight',
            'source': 'Family Profile',
            'field': 'Total Members',
            'score': score,
            'report': 'Socioeconomic',
            'variables': c.make_variables(records[0], data_point),
            'remark': get_correlation_remark(score)
        }
    )

    score = c.get_correlation_score(c.make_variables(records[1], data_point))

    scores.append(
        {
            'category': 'Height for Age - Stunted and Severely Stunted',
            'source': 'Family Profile',
            'field': 'Total Members',
            'score': score,
            'report': 'Socioeconomic',
            'variables': c.make_variables(records[1], data_point),
            'remark': get_correlation_remark(score)
        }
    )

    score = c.get_correlation_score(c.make_variables(records[2], data_point))

    scores.append(
        {
            'category': 'Weight for Height/Length - Wasted and Severely Wasted',
            'source': 'Family Profile',
            'field': 'Total Members',
            'score': score,
            'report': 'Socioeconomic',
            'variables': c.make_variables(records[2], data_point),
            'remark': get_correlation_remark(score)
        }
    )

    # education
    attainments = datapoints.educational_attainment_for_r

    for a in attainments:
        data_point = socioeconomic.get_educational_attainment(a)
        score = c.get_correlation_score(c.make_variables(records[0], data_point))

        scores.append(
            {
                'category': 'Weight for Age - Underweight and Severely Underweight',
                'source': 'Family Profile',
                'field': a,
                'score': score,
                'report': 'Socioeconomic',
                'variables': c.make_variables(records[0], data_point),
                'remark': get_correlation_remark(score)
            }
        )
    for a in attainments:
        data_point = socioeconomic.get_educational_attainment(a)
        score = c.get_correlation_score(c.make_variables(records[1], data_point))

        scores.append(
            {
                'category': 'Height for Age - Stunted and Severely Stunted',
                'source': 'Family Profile',
                'field': a,
                'score': score,
                'report': 'Socioeconomic',
                'variables': c.make_variables(records[1], data_point),
                'remark': get_correlation_remark(score)
            }
        )
    for a in attainments:
        data_point = socioeconomic.get_educational_attainment(a)
        score = c.get_correlation_score(c.make_variables(records[2], data_point))

        scores.append(
            {
                'category': 'Weight for Height/Length - Wasted and Severely Wasted',
                'source': 'Family Profile',
                'field': a,
                'score': score,
                'report': 'Socioeconomic',
                'variables': c.make_variables(records[2], data_point),
                'remark': get_correlation_remark(score)
            }
        )

    # toilet type
    toilets = datapoints.toilet_type

    for t in toilets:
        data_point = socioeconomic.get_toilet_type(t)
        score = c.get_correlation_score(c.make_variables(records[0], data_point))

        scores.append(
            {
                'category': 'Weight for Age - Underweight and Severely Underweight',
                'source': 'Family Profile',
                'field': t,
                'score': score,
                'report': 'Socioeconomic',
                'variables': c.make_variables(records[0], data_point),
                'remark': get_correlation_remark(score)
            }
        )
    for t in toilets:
        data_point = socioeconomic.get_toilet_type(t)
        score = c.get_correlation_score(c.make_variables(records[1], data_point))

        scores.append(
            {
                'category': 'Height for Age - Stunted and Severely Stunted',
                'source': 'Family Profile',
                'field': t,
                'score': score,
                'report': 'Socioeconomic',
                'variables': c.make_variables(records[1], data_point),
                'remark': get_correlation_remark(score)
            }
        )
    for t in toilets:
        data_point = socioeconomic.get_toilet_type(t)
        score = c.get_correlation_score(c.make_variables(records[2], data_point))

        scores.append(
            {
                'category': 'Weight for Height/Length - Wasted and Severely Wasted',
                'source': 'Family Profile',
                'field': t,
                'score': score,
                'report': 'Socioeconomic',
                'variables': c.make_variables(records[2], data_point),
                'remark': get_correlation_remark(score)
            }
        )

    # food production
    ways = datapoints.food_production

    for w in ways:
        data_point = socioeconomic.get_food_production(w)
        score = c.get_correlation_score(c.make_variables(records[0], data_point))

        scores.append(
            {
                'category': 'Weight for Age - Underweight and Severely Underweight',
                'source': 'Family Profile',
                'field': w,
                'score': score,
                'report': 'Socioeconomic',
                'variables': c.make_variables(records[0], data_point),
                'remark': get_correlation_remark(score)
            }
        )
    for w in ways:
        data_point = socioeconomic.get_food_production(w)
        score = c.get_correlation_score(c.make_variables(records[1], data_point))

        scores.append(
            {
                'category': 'Height for Age - Stunted and Severely Stunted',
                'source': 'Family Profile',
                'field': w,
                'score': score,
                'report': 'Socioeconomic',
                'variables': c.make_variables(records[1], data_point),
                'remark': get_correlation_remark(score)
            }
        )
    for w in ways:
        data_point = socioeconomic.get_food_production(w)
        score = c.get_correlation_score(c.make_variables(records[2], data_point))

        scores.append(
            {
                'category': 'Weight for Height/Length - Wasted and Severely Wasted',
                'source': 'Family Profile',
                'field': w,
                'score': score,
                'report': 'Socioeconomic',
                'variables': c.make_variables(records[2], data_point),
                'remark': get_correlation_remark(score)
            }
        )

    # WATER SOURCES
    ws = datapoints.water_sources

    for w in ws:
        data_point = socioeconomic.get_water_source(w)
        score = c.get_correlation_score(c.make_variables(records[0], data_point))

        scores.append(
            {
                'category': 'Weight for Age - Underweight and Severely Underweight',
                'source': 'Family Profile',
                'field': w,
                'score': score,
                'report': 'Socioeconomic',
                'variables': c.make_variables(records[0], data_point),
                'remark': get_correlation_remark(score)
            }
        )
    for w in ws:
        data_point = socioeconomic.get_water_source(w)
        score = c.get_correlation_score(c.make_variables(records[1], data_point))

        scores.append(
            {
                'category': 'Height for Age - Stunted and Severely Stunted',
                'source': 'Family Profile',
                'field': w,
                'score': score,
                'report': 'Socioeconomic',
                'variables': c.make_variables(records[1], data_point),
                'remark': get_correlation_remark(score)
            }
        )
    for w in ws:
            data_point = socioeconomic.get_water_source(w)
            score = c.get_correlation_score(c.make_variables(records[2], data_point))

            scores.append(
                {
                    'category': 'Weight for Height/Length - Wasted and Severely Wasted',
                    'source': 'Family Profile',
                    'field': w,
                    'score': score,
                    'report': 'Socioeconomic',
                    'variables': c.make_variables(records[2], data_point),
                    'remark': get_correlation_remark(score)
                }
            )

    return scores


def create_correlation_session(request):

    request.session['micronutrient'] = trim_correlations(display_micronutrient([]))
    request.session['maternal'] = trim_correlations(display_maternal([]))
    request.session['socioeconomic'] = trim_correlations(display_socioeconomic([]))
    request.session['child_care'] = trim_correlations(display_child_care([]))


def get_correlation_remark(score):


    if 1 >= abs(score) >= 0.7:
        return "Strong"

    elif 0.7 > abs(score) >= 0.5:
        return "Mild"

    elif 0.5 > abs(score) > 0:
        return "Weak"

    return "No Correlation"


def trim_correlations(scores):

    return [s for s in scores if s['score'] > 0]


