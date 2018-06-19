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

    # ajax
    path('nutritional_status/get_weights', views.get_nutritional_status, name='get_weights'),
    path('micronutrient/get_data', views.get_micronutrient, name='get_micronutrient')
]