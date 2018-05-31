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
    path('bns/monthly_reweighing', views.monthly_reweighing_index, name='monthly_reweighing_index')
]