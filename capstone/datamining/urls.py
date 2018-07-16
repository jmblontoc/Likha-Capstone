from django.conf import urls
from django.urls import path

from datamining import views

app_name = 'datamining'

urlpatterns = [
    path('', views.index, name='index'),

    # forecasts
    path('forecast/<int:id>', views.forecast, name='forecast'),

    # ajax
    path('get_variables', views.get_variables, name='get_variables'),

# ajax
    path('get_variables_v2', views.get_variables_v2, name='get_variables_v2'),
]