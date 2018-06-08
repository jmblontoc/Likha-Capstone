from django.urls import path

from datapreprocessing import views

app_name = 'datapreprocessing'

urlpatterns = [
    path('', views.index, name='index'),

    # add data map
    path('add_metric', views.add_metric, name='add_metric')
]