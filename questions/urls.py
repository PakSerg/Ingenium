from django.urls import path
from .views import *


app_name = 'questions'

urlpatterns = [
    path('all-questions/', AllQuestionsView.as_view(), name='all_questions'), 
    path('<int:year>/<int:month>/<int:day>/<slug:question>/', SingleQuestionView.as_view(), name='single_question'), 
    path('<slug:category>', CategoryView.as_view(), name='category'), 
    path('<slug:tag>', TagView.as_view(), name='tag')
]