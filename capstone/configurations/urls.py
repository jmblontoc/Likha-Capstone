from django.urls import path

from configurations import views

app_name = 'conf'
urlpatterns = [

    path('', views.index, name='index'),

    path('set_correlations', views.set_correlations, name='set_correlations'),

    # notification to BNS
    path('notify_bns', views.set_notification_time, name='notify_bns')
]