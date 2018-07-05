from django.urls import path

from datainput import views

app_name = 'datainput'

urlpatterns = [
    path('bns/eOPT/file', views.handle_opt_file, name='handle_opt_file'),

    # show opt records
    path('bns/eOPT/list', views.show_opt_list, name='show_opt_list'),

    # show eOPT file
    path('bns/eOPT/show/<int:id>', views.view_opt_file, name='view_opt_file'),

    # show OPT! KAMMY here
    path('bns/eOPT/display/<int:id>', views.display_opt, name='display_opt'),

    # show fhsis records
    path('bns/fhsis/list', views.show_fhsis_list, name='show_fhsis_list'),

    # show fhsis file
    path('bns/fhsis/show/<int:id>', views.view_fhsis_file, name='view_fhsis_file'),

    # complete errors
    path('bns/fhsis/validate', views.complete_fields, name='complete_fields'),

    # display fhsis
    path('bns/fhsis/display/<int:id>', views.display_fhsis, name='display_fhsis'),

    path('bns/family_profile/file', views.handle_family_profile_file, name='handle_family_profile_file'),
    path('bns/family_profile/list', views.family_profiles, name='family_profiles'),

    # view current family profile
    path('bns/family_profile/view_current', views.view_family_uploaded, name='view_current_fp'),

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

    # fhsis
    path('bns/fhsis/upload', views.handle_fhsis_file, name='handle_fhsis_file'),

    # archives
    path('bns/archives', views.reports_archive, name='archives'),

    # select from archive
    path('bns/archives/select', views.select_report, name='select_report'),

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
    path('nutritionist/unemployment_rate', views.unemployment_rate_index, name='unemployment_rate_index'),

    # data status index
    path('nutritionist/data_status', views.data_status_index, name='data_status_index'),

    # show opt
    path('nutritionist/data_status/<int:id>/opt', views.show_opt, name='show_opt'),

    # opt evaluation
    path('nutritionist/data_status/<int:id>/opt/<int:opt_id>/evaluate', views.evaluate_opt, name='evaluate_opt'),

    # accept opt
    path('nutritionist/data_status/<int:id>/opt/accept/<int:opt_id>', views.accept_opt, name='accept_opt'),

    # reject opt
    path('nutritionist/data_status/<int:id>/opt/reject/<int:opt_id>', views.reject_opt, name='reject_opt'),

    # show fhsis
    path('nutritionist/data_status/<int:id>/fhsis', views.show_fhsis, name='show_fhsis'),

    # accept fhsis
    path('nutritionist/data_status/<int:id>/fhsis/accept/<int:fhsis_id>', views.accept_fhsis, name='accept_fhsis'),

    # reject fhsis
    path('nutritionist/data_status/<int:id>/fhsis/reject/<int:fhsis_id>', views.reject_fhsis, name='reject_fhsis'),

    # view reweighing
    path('nutritionist/data_status/<int:id>/reweighing', views.view_reweighing, name='view_reweighing'),

    # accept reweighing
    path('nutritionist/data_status/<int:id>/reweighing/accept', views.accept_reweighing, name='accept_reweighing'),

    # reject reweighing
    path('nutritionist/data_status/<int:id>/reweighing/reject', views.reject_reweighing, name='reject_reweighing'),

    # show list of family profile records
    path('nutritionist/data_status/<int:id>/family_profiles', views.show_family_profiles, name='show_family_profiles'),

    # accept family profiles
    path('nutritionist/data_status/<int:id>/family_profiles/accept', views.accept_family_profiles, name='accept_family_profiles'),

    # reject family profiles
    path('nutritionist/data_status/<int:id>/family_profiles/reject', views.reject_family_profiles, name='reject_family_profiles'),

    # nutritionist archives of barangay reports
    path('nutritionist/archives/barangay_reports/', views.barangay_archives, name='barangay_archives'),

    # select report by nutritionist
    path('nutritionist/archives/select', views.select_report_nutritionist, name='select_report_nutritionist')
]