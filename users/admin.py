from django.contrib import admin
from .models import User 


@admin.register(User) 
class UserAdmin(admin.ModelAdmin): 
    list_display = ['pk', 'email', 'username', 'grade', 'given_answers_count', 'image']
    list_filter = ['last_login']