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
]