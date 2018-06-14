
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from friends.datamining import correlations
from datainput.models import NutritionalStatus, Barangay, Sex, ChildCare, Tuberculosis, Malaria, Immunization, \
    MaternalCare, Schistosomiasis, Leprosy, Flariasis, STISurveillance
from friends.datapreprocessing import checkers
from django.shortcuts import render, redirect
from friends import datapoints


# Create your views here.

@login_required
def index(request):

    if checkers.is_updated():

        nutritional_statuses = NutritionalStatus.objects.all()

        scores = []

        # # # # # # # # # # # # #
        # FEMALE
        sex = Sex.objects.get(name='Female')
        sex2 = Sex.objects.get(name='Male')

        # for status in nutritional_statuses:
        #     # child care
        #     for data in datapoints.get_child_care_fields():
        #         phrase = str(data).split(".")
        #         field = phrase[2]
        #
        #         weights = correlations.get_weight_values_per_month(status, sex)
        #         data_point = correlations.get_fhsis(ChildCare, field, sex)
        #         score = correlations.get_correlation_score(
        #             correlations.make_variables(weights, data_point)
        #         )
        #
        #         scores.append(
        #             {
        #                 'category': status.name + " - Female",
        #                 'source': 'Child Care',
        #                 'field': data.verbose_name,
        #                 'score': score
        #             }
        #         )
        #
        # for status in nutritional_statuses:
        #
        #     # tuberculosis
        #     for data in datapoints.get_tb_fields():
        #         phrase = str(data).split(".")
        #         field = phrase[2]
        #
        #         weights = correlations.get_weight_values_per_month(status, sex)
        #         data_point = correlations.get_fhsis(Tuberculosis, field, sex)
        #         score = correlations.get_correlation_score(
        #             correlations.make_variables(weights, data_point)
        #         )
        #
        #         scores.append(
        #             {
        #                 'category': status.name + " - Female",
        #                 'source': 'Tuberculosis',
        #                 'field': data.verbose_name,
        #                 'score': score
        #             }
        #         )

        correlations.display(
            datapoints.get_child_care_fields(),
            scores,
            ChildCare,
            sex
        )

        correlations.display(
            datapoints.get_tb_fields(),
            scores,
            Tuberculosis,
            sex
        )

        correlations.display(
            Malaria._meta.get_fields()[1:6],
            scores,
            Malaria,
            sex
        )

        correlations.display(
            Immunization._meta.get_fields()[1:4],
            scores,
            Immunization,
            sex
        )

        correlations.display(
            Schistosomiasis._meta.get_fields()[1:3],
            scores,
            Schistosomiasis,
            sex
        )

        correlations.display(
            Leprosy._meta.get_fields()[1:3],
            scores,
            Leprosy,
            sex
        )

        correlations.display(
            Flariasis._meta.get_fields()[1:4],
            scores,
            Flariasis,
            sex
        )

        correlations.display_no_sex(
            MaternalCare._meta.get_fields()[1:10],
            scores,
            MaternalCare,
            sex
        )

        correlations.display_no_sex(
            STISurveillance._meta.get_fields()[2:5],
            scores,
            STISurveillance,
            sex
        )

        correlations.display(
            datapoints.get_child_care_fields(),
            scores,
            ChildCare,
            sex2
        )

        correlations.display(
            datapoints.get_tb_fields(),
            scores,
            Tuberculosis,
            sex2
        )

        correlations.display(
            Malaria._meta.get_fields()[1:6],
            scores,
            Malaria,
            sex2
        )

        correlations.display(
            Immunization._meta.get_fields()[1:4],
            scores,
            Immunization,
            sex2
        )

        correlations.display(
            Schistosomiasis._meta.get_fields()[1:3],
            scores,
            Schistosomiasis,
            sex2
        )

        correlations.display(
            Leprosy._meta.get_fields()[1:3],
            scores,
            Leprosy,
            sex2
        )

        correlations.display(
            Flariasis._meta.get_fields()[1:4],
            scores,
            Flariasis,
            sex2
        )

        correlations.display_no_sex(
            MaternalCare._meta.get_fields()[1:10],
            scores,
            MaternalCare,
            sex2
        )

        correlations.display_no_sex(
            STISurveillance._meta.get_fields()[2:5],
            scores,
            STISurveillance,
            sex2
        )

        context = {
            'statuses': nutritional_statuses,
            'scores': scores
        }

        return render(request, 'datamining/index.html', context)

    messages.error(request, 'Data is not up to date')
    return redirect('core:nutritionist')
