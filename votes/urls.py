from django.urls import path, include
from .views import *


app_name = 'votes'

urlpatterns = [
    path('question/vote-up/', vote_up_for_question, name='vote_up_for_question'),
    path('question/vote-down/', vote_down_for_question, name='vote_down_for_question'),
    path('question/delete-vote/', delete_vote_for_question, name='delete_vote_for_question'),
]