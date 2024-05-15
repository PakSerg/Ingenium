from django.urls import path, include
from .views import *


app_name = 'votes'

urlpatterns = [
    # path('question/vote-up/', vote_up, name='question-vote-up'), 
    # path('questions/vote-down/', name='question-vote-down'), 
    path('vote-for-question/', vote_for_question, name='vote_for_question'),
]