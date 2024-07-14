from django.urls import path
from .views import *


app_name = 'questions'

urlpatterns = [
    path('all-questions/', AllQuestionsView.as_view(), name='all_questions'), 
    path('all-categories/', AllCategoriesView.as_view(), name='all_categories'), 
    path('create-question/', CreateQuestionView.as_view(), name='create_question'),
    path('<int:year>/<int:month>/<int:day>/<slug:question_slug>/', SingleQuestionView.as_view(), name='single_question'),
    path('search/', SearchView.as_view(), name='search'), 
    path('category/<slug:category_slug>/', CategoryView.as_view(), name='category'), 
    path('tag/<slug:tag_slug>/', TagView.as_view(), name='tag'),
    path('get_tags/<int:category_id>', get_tags_view, name='get_tags')
]