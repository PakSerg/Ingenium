from django.db.models import Sum
from .models import VoteForQuestion, VoteType
from users.services import UserService
from questions.services import QuestionService


class VoteForQuestionService(): 
    @staticmethod 
    def vote_up(question_id: int, user_id: int) -> int: 
        old_vote = VoteForQuestionService.get_vote_or_none(question_id, user_id)
        question = QuestionService.get_published_question_by_id(question_id)

        if not old_vote:
            VoteForQuestionService.create_vote(question_id, user_id, VoteType.UP)
            question.votes_count += 1
        elif old_vote.type == VoteType.DOWN:
            old_vote.type = VoteType.UP
            old_vote.save()
            question.votes_count += 2
        else:
            raise PermissionError()

        question.save()
        return question.votes_count

    @staticmethod 
    def vote_down(question_id: int, user_id: int) -> int: 
        old_vote = VoteForQuestionService.get_vote_or_none(question_id, user_id)
        question = QuestionService.get_published_question_by_id(question_id)

        if not old_vote:
            VoteForQuestionService.create_vote(question_id, user_id, VoteType.DOWN)
            question.votes_count -= 1
        elif old_vote.type == VoteType.UP:
            old_vote.type = VoteType.DOWN
            old_vote.save()
            question.votes_count -= 2
        else:
            raise PermissionError()

        question.save()
        return question.votes_count

    @staticmethod 
    def delete_existing_vote(question_id: int, user_id: int) -> int: 
        vote_to_delete = VoteForQuestionService.get_vote(question_id, user_id)
        
        question = QuestionService.get_published_question_by_id(question_id)

        if vote_to_delete.type == VoteType.UP: 
            question.votes_count -= 1
        elif vote_to_delete.type == VoteType.DOWN: 
            question.votes_count += 1
        
        question.save()
        VoteForQuestion.delete(vote_to_delete) 
        
        return question.votes_count

    @staticmethod 
    def count_voting_result(question_id: int) -> int: 
        question = QuestionService.get_published_question_by_id(question_id)
        voting_result = VoteForQuestion.objects.filter(question=question).aggregate(
            voting_result=Sum('type')
        ).get('voting_result')
        return voting_result 
    
    @staticmethod 
    def get_vote(question_id: int, user_id: int) -> VoteForQuestion: 
        vote = VoteForQuestion.objects.get(user=UserService.get_user_by_id(user_id), 
                                        question=QuestionService.get_published_question_by_id(question_id))
        return vote
    
    @staticmethod 
    def get_vote_or_none(question_id: int, user_id: int) -> VoteForQuestion | None: 
        vote_or_none = VoteForQuestion.objects.filter(user=UserService.get_user_by_id(user_id), 
                                        question=QuestionService.get_published_question_by_id(question_id)).first() 
        return vote_or_none
    
    @staticmethod 
    def get_vote_or_create(question_id: int, user_id: int) -> tuple[VoteForQuestion, bool]:
        vote, created = VoteForQuestion.objects.get_or_create(user=UserService.get_user_by_id(user_id), 
                                        question=QuestionService.get_published_question_by_id(question_id)) 
        return vote, created
    
    @staticmethod 
    def create_vote(question_id: int, user_id: int, vote_type: VoteType) -> VoteForQuestion: 
        vote = VoteForQuestion.objects.create(user=UserService.get_user_by_id(user_id), 
                                        question=QuestionService.get_published_question_by_id(question_id), 
                                        type=vote_type) 
        vote.save()
        return vote