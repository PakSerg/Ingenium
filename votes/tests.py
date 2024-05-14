from django.test import TestCase
from .models import VoteForQuestion 
from .services import VoteForQuestionService
from users.models import User 
from questions.models import Question, Category
import string 
import random


class QuestionVoteTestCase(TestCase): 
    def setUp(self):
        self.user = User.objects.create(username='test_user', email='test@gmail.com', password='test_password')
        self.question = Question.objects.create(title='Test', content='test', user=self.user, 
                                                category=Category.objects.create(title='test', description='test'))

    def test_get_vote(self): 
        created_vote = VoteForQuestion.objects.create(user=self.user, question=self.question, type=1)
        got_vote = VoteForQuestionService.get_vote(self.question.pk, self.user.pk) 
        self.assertEqual(created_vote, got_vote)
        
    def test_vote_up(self): 
        vote = VoteForQuestionService.vote_up(self.question.pk, self.user.pk) 
        self.assertEqual(vote.type, 1)

        vote_again = VoteForQuestionService.vote_up(self.question.pk, self.user.pk) 
        self.assertEqual(vote_again.type, 1)

    def test_vote_down(self): 
        vote = VoteForQuestionService.vote_down(self.question.pk, self.user.pk) 
        self.assertEqual(vote.type, -1)

        vote_again = VoteForQuestionService.vote_down(self.question.pk, self.user.pk) 
        self.assertEqual(vote_again.type, -1)

    def test_delete_vote(self): 
        VoteForQuestionService.vote_down(self.question.pk, self.user.pk) 
        VoteForQuestionService.delete_existing_vote(self.question.pk, self.user.pk)
        self.assertFalse(VoteForQuestion.objects.filter(question=self.question, user=self.user).exists())

    def test_calculate_voting_result(self): 
        for _ in range(100):
            user_to_like = User.objects.create(username=generate_random_string(10), email=generate_random_email(15), password='test_password')
            VoteForQuestionService.vote_up(self.question.pk, user_to_like.pk)
        for _ in range(10): 
            user_to_dislike = User.objects.create(username=generate_random_string(10), email=generate_random_email(15), password='test_password')
            VoteForQuestionService.vote_down(self.question.pk, user_to_dislike.pk)

        self.assertEqual(VoteForQuestionService.count_voting_result(self.question.pk), 90)

    def get_vote_or_create(self): 
        self.assertFalse(VoteForQuestion.objects.filter(question=self.question, user=self.user))

        created_vote = VoteForQuestionService.get_vote_or_create(self.question.pk, self.user.pk)
        got_vote = VoteForQuestionService.get_vote_or_create(self.question.pk, self.user.pk) 

        self.assertEqual(created_vote, got_vote)

        


def generate_random_string(length) -> str:
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length)) 

def generate_random_email(length) -> str:
    username = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
    domain = 'example.com'  
    return f"{username}@{domain}"