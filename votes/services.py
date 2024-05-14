from .models import VoteForQuestion
from django.db.models import Sum
from users.services import UserService
from questions.services import QuestionService


class VoteForQuestionService(): 
    @staticmethod 
    def vote_up(question_id: int, user_id: int) -> VoteForQuestion: 
        vote = VoteForQuestionService.get_vote_or_create(question_id, user_id)
        vote.type = 1
        vote.save()

        return vote

    @staticmethod 
    def vote_down(question_id: int, user_id: int) -> None: 
        vote = VoteForQuestionService.get_vote_or_create(question_id, user_id)
        vote.type = -1
        vote.save()
        
        return vote

    @staticmethod 
    def delete_existing_vote(question_id: int, user_id: int) -> None: 
        vote = VoteForQuestionService.get_vote(user_id, question_id)
        VoteForQuestion.delete(vote) 

    @staticmethod 
    def count_voting_result(question_id: int) -> int: 
        question = QuestionService.get_question_by_id(question_id)
        voting_result = VoteForQuestion.objects.filter(question=question).aggregate(
            voting_result=Sum('type')
        ).get('voting_result')
        return voting_result 
    
    @staticmethod
    def get_vote(question_id: int, user_id: int) -> VoteForQuestion: 
        vote = VoteForQuestion.objects.get(user=UserService.get_user_by_id(user_id), 
                                        question=QuestionService.get_question_by_id(question_id)) 
        return vote
    
    @staticmethod 
    def get_vote_or_create(question_id: int, user_id: int) -> VoteForQuestion: 
        vote, _ = VoteForQuestion.objects.get_or_create(user=UserService.get_user_by_id(user_id), 
                                        question=QuestionService.get_question_by_id(question_id)) 
        return vote
    