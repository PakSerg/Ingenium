from django import template
from django.db.models import Count 
from django.db.models.query import QuerySet
from ..services import CategoryService
from ..models import Category


register = template.Library()

@register.inclusion_tag('questions/includes/sidebar.html')  
def show_sidebar_categories() -> QuerySet[Category]: 
	categories =  CategoryService.get_all_categories()
	return {'categories': categories}
