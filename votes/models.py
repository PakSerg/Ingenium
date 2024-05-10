from django.db import models
from users.models import User
from questions.models import Question


class QuestionVote(models.Model): 

    class VoteType(models.IntegerChoices): 
        UP = 1, 'Лайк'
        DOWN = -1, 'Дизлайк'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_votes') 
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='votes') 
    type = models.IntegerField(choices=VoteType.choices, default=VoteType.UP)
    