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

    # delete root cause
    path('root_cause/delete/<int:id>', views.delete_root_cause, name='delete_root_cause'),

    # create root cause
    path('create_causal_model', views.create_causal_model, name='create_causal_model'),

    # ajax
    path('root_cause/add/ajax', views.insert_root_cause, name='ajax_add_root_cause'),

    path('create_tree', views.insert_blocks, name='create_tree'),

    # produce causal model
    path('produce_causal_model', views.produce_causal_model, name='produce_causal_model'),

    # details ajax
    path('details', views.get_blocks, name='details_ajax'),

    path('details2', views.get_blocks_2, name='details2'),

    # add comment
    path('insert_comment', views.insert_comment, name='insert_comment'),

    # approve causal model
    path('approve', views.approve_model, name='approve_causal_model'),

    # view summary
    path('root_cause/view_summary/<int:metric>/', views.view_summary, name='view_summary'),

    # ajax
    path('view_summary_ajax', views.ajax_get_metric, name='get_metric_ajax'),

    path('dummy', views.dummy, name='dummy'),

    path('p', views.get_boxes, name='p'),

    path('add_customized', views.append_to_causal_model, name='append_to_causal_model'),

    path('add_intervention_from_modal', views.add_intervention_from_modal, name='add_intervention_from_modal'),

    # causal model report
    path('causal_model/<int:year>/', views.causal_model_report, name='causal_model_report')


]