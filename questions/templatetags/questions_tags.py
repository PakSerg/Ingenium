from django import template
from django.db.models.query import QuerySet
from django.core.cache import cache
from ingenium.settings import CacheKeys
from ..services import CategoryService
from ..models import Category, Question 
from ..forms import SearchForm


register = template.Library()


@register.inclusion_tag('questions/includes/sidebar.html')  
def show_sidebar_categories() -> QuerySet[Category]: 
	categories = cache.get_or_set(key=CacheKeys.Static.ALL_CATEGORIES, 
							   default=CategoryService.get_all_categories, 
							   timeout=60 * 60 * 6)
	return {'categories': categories}


@register.inclusion_tag('questions/includes/question_in_list.html') 
def show_question_in_list(question_in_list: Question): 
	context = {'question': question_in_list}
	return context 

@register.inclusion_tag('questions/includes/question_in_list_without_category.html') 
def show_question_in_list_without_category(question_in_list: Question): 
	context = {'question': question_in_list}
	return context 


@register.inclusion_tag('questions/includes/search_form.html') 
def show_search_form(): 
	form = SearchForm()
	context = {'form': form}
	return context 