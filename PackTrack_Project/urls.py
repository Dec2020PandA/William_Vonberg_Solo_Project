"""PackTrack_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from App_PackTrack.models import User,Pet,Body,User_diary,Pet_diary,Bug,Comment

class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User,UserAdmin)

class PetAdmin(admin.ModelAdmin):
    pass
admin.site.register(Pet,PetAdmin)

class BodyAdmin(admin.ModelAdmin):
    pass
admin.site.register(Body,BodyAdmin)

class BugAdmin(admin.ModelAdmin):
    pass
admin.site.register(Bug,BugAdmin)

class User_diaryAdmin(admin.ModelAdmin):
    pass
admin.site.register(User_diary,User_diaryAdmin)

class Pet_diaryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Pet_diary,Pet_diaryAdmin)

class CommentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Comment,CommentAdmin)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('App_PackTrack.urls')),
]
