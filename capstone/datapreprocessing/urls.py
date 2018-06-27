from django.urls import path

from datapreprocessing import views

app_name = 'datapreprocessing'

urlpatterns = [
    path('', views.index, name='index'),

    # add metric
    path('add_metric', views.add_metric, name='add_metric'),

    # delete metric
    path('delete_metric/<int:id>', views.delete_metric, name='delete_metric'),

    # edit metric
    path('edit_metric/<int:id>', views.edit_metric, name='edit_metric'),
]