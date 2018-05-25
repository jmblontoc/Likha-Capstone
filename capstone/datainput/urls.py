from django.urls import path

from datainput import views

app_name = 'datainput'

urlpatterns = [
    path('bns/eOPT/file', views.handle_opt_file, name='handle_opt_file')
]