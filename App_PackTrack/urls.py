from django.urls import path
from . import views

urlpatterns = [
    path('', views.to_landing),
    path('landing',views.landing),
    path('login',views.login),
    path('register',views.register),
    path('log_page',views.log_page),
    path('reg_page',views.reg_page),
    path('login_user',views.user_login),
    path('create_user',views.create_user),
    path('summary',views.summary),
    path('profile',views.profile),
    path('logout',views.logout),
    path('user_update',views.user_update),
    path('support',views.support),
    path('process_issue',views.process_issue),
    path('pet_profile/<int:dog_tag>',views.pet_profile),
    path('add_dog',views.add_dog),
    path('pet_update/<int:dog_id>',views.pet_update),
    path('delete/<int:dog_tag>',views.delete),
    path('support_comment',views.support_comment),
    path('landing_comment',views.landing_comment),
    path('user_entry',views.user_entry),
    path('pet_entry',views.pet_entry),
]