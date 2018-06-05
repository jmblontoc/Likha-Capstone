from django.urls import path

from datapreprocessing import views

app_name = 'data-pre_processing'

urlpatterns = [
    path('', views.index, name='index')
]