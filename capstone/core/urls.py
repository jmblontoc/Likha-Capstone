from django.urls import path

from core import views

app_name = 'core'

urlpatterns = [
    path('', views.redirect_view, name='redirect_view'),
    path('login/', views.SignInView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

    # BNS index
    path('bns/', views.bns_index, name='bns-index'),

    # Nutritionist index
    path('nutritionist/', views.nutritionist, name='nutritionist'),

    # mark notification as read
    path('notification/mark_read/<int:id>', views.mark_as_read, name='mark_as_read')
]