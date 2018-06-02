from django.urls import path

from datainput import views

app_name = 'datainput'

urlpatterns = [
    path('bns/eOPT/file', views.handle_opt_file, name='handle_opt_file'),

    path('bns/family_profile/file', views.handle_family_profile_file, name='handle_family_profile_file'),
    path('bns/family_profile/list', views.family_profiles, name='family_profiles'),

    # add family profile
    path('bns/family_profile/add', views.add_family_profile, name='add_family'),

    # list of family profiles
    path('bns/family_profile/<int:id>/', views.show_profiles, name='show_profiles'),

    # ajax of showing profile
    path('bns/family_profile/show_ajax', views.show_profile_ajax, name='show_profile_ajax'),

    # monthly reweighing
    path('bns/monthly_reweighing', views.monthly_reweighing_index, name='monthly_reweighing_index'),

    # add patient
    path('bns/monthly_reweighing/add_patient', views.add_patient, name='add_patient'),

    # patient overview
    path('patient/<int:id>', views.patient_overview, name='patient_overview'),

    # monthly reweigh
    path('patient/<int:id>/reweigh', views.reweigh, name='reweigh'),

    # # # # # # # # # NUTRITIONIST URLS BELOW # # # # # # # # # #

    # nutritionist data upload
    path('nutritionist/upload/', views.nutritionist_upload, name='nutritionist_upload'),

    # health care waste management
    path('nutritionist/health_care_waste_management/', views.health_care_waste_management_index,
         name='health_care_index'),

    # add hcwm
    path('nutritionist/health_care_waste_management/add', views.add_hcwm, name='add_hcwm'),

    # ajax show hcwm
    path('nutritionist/show_health_care', views.get_health_care_waste_record, name='show_hc'),

    # informal settlers index
    path('nutritionist/informal_settlers', views.informal_settlers_index, name='informal_settlers_index'),

    # unemployment rate
    path('nutritionist/unemployment_rate', views.unemployment_rate_index, name='unemployment_rate_index')
]