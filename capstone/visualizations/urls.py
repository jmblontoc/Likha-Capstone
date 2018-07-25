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