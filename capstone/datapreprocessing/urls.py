from django.urls import path

from datapreprocessing import views

app_name = 'datapreprocessing'

urlpatterns = [
    path('', views.index, name='index'),

    # set threshold
    path('set_thresholds', views.set_thresholds, name='set_thresholds'),





    # add metric
    path('add_metric', views.add_metric, name='add_metric'),

    # delete metric
    path('delete_metric/<int:id>', views.delete_metric, name='delete_metric'),

    # edit metric
    path('edit_metric/<int:id>', views.edit_metric, name='edit_metric'),

    # # # # # # # # # DEFAULT # # # # # # # # #

    path('default/nutritional_status/', views.set_nutritional_status, name='set_nutritional_status'),

    path('default/micronutrient', views.set_micronutrient, name='set_micronutrient'),

    path('default/maternal', views.set_maternal, name='set_maternal'),

    path('default/child_care', views.set_child_care, name='set_child_care'),

    path('default/socioeconomic', views.set_socioeconomic, name='set_socioeconomic'),


    # # # # # # # # # AJAX # # # # # # # # #

    path('default/ajax', views.view_threshold, name='view_threshold_ajax'),

    path('ajax/add_metric', views.add_metric_ajax, name='add_metric_ajax'),

    path('ajax/get_values', views.get_value_for_threshold, name='ajax_get_values'),

    path('ajax/insert_metric', views.insert_metric_ajax, name='insert_metric')
]