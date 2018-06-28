from django.urls import path

from causalmodel import views

app_name = 'causalmodel'

urlpatterns= [
    path('', views.index, name='index'),

    # RC index
    path('root_cause/', views.root_causes, name='rc_index'),

    # add root cause
    path('root_cause/add', views.add_root_cause, name='add_root_cause'),

    # create root cause
    path('create_causal_model', views.create_causal_model, name='create_causal_model'),

    # ajax
    path('root_cause/add/ajax', views.insert_root_cause, name='ajax_add_root_cause')
]