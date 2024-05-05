from django import template
from django.db.models import Count 
from django.db.models.query import QuerySet
from ..services import CategoryService
from ..models import Category, Question


register = template.Library()

@register.inclusion_tag('questions/includes/sidebar.html')  
def show_sidebar_categories() -> QuerySet[Category]: 
	categories =  CategoryService.get_all_categories()
	return {'categories': categories}

@register.inclusion_tag('questions/includes/question_in_list.html') 
def show_question_in_list(question_in_list: Question): 
	context = {'question': question_in_list}
	return context