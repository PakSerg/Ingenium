from django.urls import path
from .views import *


app_name = 'questions'

urlpatterns = [
    path('all-questions/', AllQuestionsView.as_view(), name='all_questions'), 
    path('all-categories/', AllCategoriesView.as_view(), name='all_categories'),
    path('<int:year>/<int:month>/<int:day>/<slug:question_slug>/', SingleQuestionView.as_view(), name='single_question'), 
    path('<slug:category_slug>/', CategoryView.as_view(), name='category'), 
    path('<slug:tag_slug>/', TagView.as_view(), name='tag')
]