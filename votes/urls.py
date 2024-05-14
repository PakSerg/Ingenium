from django.urls import path, include
from .views import *


app_name = 'votes'

urlpatterns = [
    path('vote-for-question/', vote_for_question, name='vote_for_question')
]