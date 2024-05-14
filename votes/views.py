from django.http import JsonResponse 
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .services import VoteForQuestionService
from questions.services import QuestionService
from users.models import User 
from questions.models import Question 
from .models import VoteForQuestion
from django.db import transaction


@require_POST
@login_required
def vote_for_question(request): 
    user_id = request.POST.get('user_id') 
    question_id = request.POST.get('question_id')
    vote_type = request.POST.get('vote_type') 

    if not user_id or not vote_type or not question_id or vote_type not in ('up', 'down', 'delete'): 
        return JsonResponse({'status': 'error', 'message': 'invalid input'}) 
    
    try: 
        match vote_type: 
            case 'up': 
                QuestionService.increment_votes_count(question_id)
                VoteForQuestionService.vote_up(question_id, user_id) 
                
            case 'down':
                QuestionService.decrement_votes_count(question_id)
                VoteForQuestionService.vote_down(question_id, user_id) 

            case 'delete': 
                vote = VoteForQuestionService.get_vote(question_id, user_id)
                
                if vote.type == 1: 
                    QuestionService.decrement_votes_count(question_id) 
                elif vote.type == -1:
                    QuestionService.increment_votes_count(question_id) 

                VoteForQuestionService.delete_existing_vote(question_id, user_id) 
                    
            case _:
                raise Exception
            
        votes_count = QuestionService.get_question_by_id(question_id).votes_count
        return JsonResponse({'status': 'ok', 'votes_count': votes_count}) 
            
    except (User.DoesNotExist, Question.DoesNotExist, VoteForQuestion.DoesNotExist): 
        return JsonResponse({'status': 'error', 
                             'message': 'no such user, question or vote found'}) 
    except:
        return JsonResponse({'status': 'error', 
                             'message': 'unknown exception'}) 

    
    