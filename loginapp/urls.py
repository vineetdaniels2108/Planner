from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('show_login_page', views.show_login_page), 
    path('show_reg_page', views.show_reg_page),
    path('show_user_info/<int:user_id>', views.show_user_info),
    path('create_user', views.create_user),
    path('user_login', views.user_login),
    path('show_planner_profile', views.show_planner_profile),
    path('show_cust_profile', views.show_cust_profile),
    path('create_planner_profile', views.create_planner_profile),
    path('create_customer_profile', views.create_customer_profile),
    path('leave_message', views.leave_message),
    path('leave_comment', views.leave_comment),
    path('show_profile_page', views.show_profile_page),
    path('delete/<int:user_id>', views.delete),
    path('logout', views.logout),
]
