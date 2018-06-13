from django.conf import urls
from django.urls import path

from datamining import views

app_name = 'datamining'

urlpatterns = [
    path('', views.index, name='index'),
]