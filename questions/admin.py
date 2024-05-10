from django.contrib import admin
from .models import Question, Category, Tag, Answer


@admin.register(Question) 
class QuestionAdmin(admin.ModelAdmin): 
    list_display = ['title', 'content', 'category', 'user', 'created_at', 'votes_count', 'status']
    list_filter = ['created_at'] 
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['created_at', 'votes_count']
    raw_id_fields = ['tags']


@admin.register(Category) 
class CategoryAdmin(admin.ModelAdmin): 
    list_display = ['title', 'description', 'slug'] 
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Tag) 
class TagAdmin(admin.ModelAdmin): 
    list_display = ['text', 'slug', 'category']
    prepopulated_fields = {'slug': ('text',)}
    ordering = ['category']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin): 
    list_display = ['content', 'question', 'user', 'votes_count'] 