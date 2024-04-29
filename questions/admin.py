from django.contrib import admin
from .models import Question, Category


@admin.register(Question) 
class UserAdmin(admin.ModelAdmin): 
    list_display = ['title', 'content', 'category', 'user', 'created_at', 'votes']
    list_filter = ['created_at'] 
    


@admin.register(Category) 
class CategoryAdmin(admin.ModelAdmin): 
    list_display = ['title', 'description'] 
