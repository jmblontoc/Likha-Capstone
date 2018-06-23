from django.urls import path

from visualizations import views

app_name = 'visualizations'
urlpatterns = [

    # index
    path('', views.index, name='index'),

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
    path('nutritional_status/get_weights', views.get_nutritional_status, name='get_weights'),
    path('micronutrient/get_data', views.get_micronutrient, name='get_micronutrient'),
    path('maternal/get_data', views.get_maternal, name='get_maternal'),
    path('child_care/get_data', views.get_child_care, name='get_child_care')
]