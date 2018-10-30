from django.urls import path

from configurations import views

app_name = 'conf'
urlpatterns = [

    path('', views.index, name='index'),

    path('set_correlations', views.set_correlations, name='set_correlations'),

    # notification to BNS
    path('notify_bns', views.set_notification_time, name='notify_bns'),

    # suggested interventions
    path('set_interventions', views.set_suggested_interventions, name='set_interventions'),

    # ajax
    path('get_interventions', views.ajax_get_intervetions, name='get_interventions'),
    path('ajax_set_interventions', views.ajax_set_interventions, name='ajax_set_interventions')
]