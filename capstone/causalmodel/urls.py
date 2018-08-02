from django.urls import path

from causalmodel import views

app_name = 'causalmodel'

urlpatterns = [
    path('<int:year>/', views.index, name='index'),

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

    # produce causal model
    path('produce_causal_model', views.produce_causal_model, name='produce_causal_model'),

    # details ajax
    path('details', views.get_blocks, name='details_ajax'),

    # add comment
    path('insert_comment', views.insert_comment, name='insert_comment'),

    # approve causal model
    path('approve', views.approve_model, name='approve_causal_model'),

    # view summary
    path('root_cause/view_summary/<int:metric>/', views.view_summary, name='view_summary'),

    # ajax
    path('view_summary_ajax', views.ajax_get_metric, name='get_metric_ajax'),

    path('dummy', views.dummy, name='dummy'),

    path('p', views.get_boxes, name='p')


]