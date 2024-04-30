from django.contrib import admin
from .models import Question, Category, Tag


@admin.register(Question) 
class QuestionAdmin(admin.ModelAdmin): 
    list_display = ['title', 'content', 'category', 'user', 'created_at', 'votes']
    list_filter = ['created_at'] 
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['created_at', 'votes']


@admin.register(Category) 
class CategoryAdmin(admin.ModelAdmin): 
    list_display = ['title', 'description', 'slug'] 
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Tag) 
class TagAdmin(admin.ModelAdmin): 
    list_display = ['text', 'slug', 'category']
    prepopulated_fields = {'slug': ('text',)}
    ordering = ['category']
