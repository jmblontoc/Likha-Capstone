from django.urls import path

from core import views

app_name = 'core'

urlpatterns = [
    path('login', views.SignInView.as_view(), name='login'),
    path('logout', views.logout_view, name='logout'),

    # BNS index
    path('bns/', views.bns_index, name='bns-index')
]