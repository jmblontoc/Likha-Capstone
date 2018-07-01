from django.urls import path

from causalmodel import views

app_name = 'causalmodel'

urlpatterns= [
    path('', views.index, name='index'),

    # details
    path('<int:id>/', views.details, name='details'),

    # RC index
    path('root_cause/', views.root_causes, name='rc_index'),

    # add root cause
    path('root_cause/add', views.add_root_cause, name='add_root_cause'),

    # create root cause
    path('create_causal_model', views.create_causal_model, name='create_causal_model'),

    # ajax
    path('root_cause/add/ajax', views.insert_root_cause, name='ajax_add_root_cause'),

    path('create_tree', views.insert_blocks, name='create_tree'),

    # details ajax
    path('details', views.get_blocks, name='details_ajax')
]