from django.urls import path

from visualizations import views

app_name = 'visualizations'
urlpatterns = [

    # index
    path('', views.index, name='index'),

    # insights city nut status
    path('city_nutritional_status', views.city_nutritional_status, name='city_nutritional_status'),

    # micronutrient
    path('city_micronutrient', views.city_micronutrient, name='city_micronutrient'),

    # maternal
    path('city_maternal', views.city_maternal, name='city_maternal'),

    # child care
    path('city_children', views.city_children_care, name='children_care'),

    # # # # # # # REPORTS # # # # # # #
    path('reports/nutritional_status/<int:year>', views.report1, name='report1'),
    path('reports/socioeconomic/<int:year>', views.report2, name='report2'),
    path('reports/micronutrient/<int:year>', views.report3, name='report3'),
    path('reports/child_care/<int:year>', views.report4, name='report4'),
    path('reports/maternal/<int:year>', views.report5, name='report5'),

    path('print/nutritional_status/<int:year>', views.print1, name='print1'),
    path('print/socioeconomic/<int:year>', views.print2, name='print2'),
    path('print/micronutrient/<int:year>', views.print3, name='print3'),
    path('print/child_care/<int:year>', views.print4, name='print4'),
    path('print/maternal/<int:year>', views.print5, name='print5'),

    # REPORTS FACILITY
    path('reports_facility', views.reports_facility, name='reports_facility'),

    # REPORTS LIBRARY
    path('reports_library', views.reports_library, name='reports_library'),

    # SAVED
    path('saved/nutritional_status/<int:year>', views.saved_report1, name='saved1'),
    path('saved/micronutrient/<int:year>', views.saved_report3, name='saved3'),
    path('saved/socioeconomic/<int:year>', views.saved_report2, name='saved2'),
    path('saved/child_care/<int:year>', views.saved_report4, name='saved4'),
    path('saved/maternal/<int:year>', views.saved_report5, name='saved5'),

    # # # # # # AJAX # # # # # # #

    path('ajax_highest', views.get_highest_barangay, name='get_highest_barangay'),
    path('ajax_top3_mns', views.top3_barangay_mns, name='top3_mns'),





















    # nutritional status
    path('nutritional_status', views.nutritional_status_report, name='nutritional_status'),

    # micronutrient
    path('micronutrient', views.micronutrient_report, name='micronutrient'),

    # maternal
    path('maternal', views.maternal_report, name='maternal'),

    # child care
    path('child_care', views.child_care, name='child_care'),

    # display report
    path('display_report', views.display_report, name='display_report'),

    # ajax
    path('nutritional_status/get_data', views.get_nutritional_status, name='get_weights'),
    path('micronutrient/get_data', views.get_micronutrient, name='get_micronutrient'),
    path('maternal/get_data', views.get_maternal, name='get_maternal'),
    path('child_care/get_data', views.get_child_care, name='get_child_care')
]