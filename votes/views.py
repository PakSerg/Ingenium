from django.http import JsonResponse 
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .services import VoteForQuestionService
from questions.services import QuestionService
from users.models import User 
from questions.models import Question 
from .models import VoteForQuestion
from django.db import transaction
    
    
# @transaction.atomic
# @require_POST
# @login_required
# def vote_up(request): 
#     question_id = request.POST.get('question_id')
#     user_id = request.POST.get('user_id')

#     if not all((question_id, user_id)): 
#         return JsonResponse({'status': 'error', 
#                              'message': 'invalid input'}) 
    
#     try: 
#         votes_count = VoteForQuestionService.vote_up(question_id, user_id)
#         return JsonResponse({'status': 'ok', 
#                              'votes_count': votes_count}) 
#     except Exception as e: 
#         if isinstance(e, (User.DoesNotExist, Question.DoesNotExist, VoteForQuestion.DoesNotExist)):
#             message = 'no such user, question or vote found'
#         elif isinstance(e, PermissionError):
#             message = 'already voted'
#         else:
#             message = f'unknown exception: {e.args}'
#         return JsonResponse({'status': 'error', 'message': message})
    

# @transaction.atomic
# @require_POST
# @login_required
# def vote_down(request): 
#     question_id = request.POST.get('question_id')
#     user_id = request.POST.get('user_id')

#     if not all((question_id, user_id)): 
#         return JsonResponse({'status': 'error', 
#                              'message': 'invalid input'}) 
    
#     try: 
#         votes_count = VoteForQuestionService.vote_down(question_id, user_id)
#         return JsonResponse({'status': 'ok', 
#                              'votes_count': votes_count}) 
#     except Exception as e: 
#         if isinstance(e, (User.DoesNotExist, Question.DoesNotExist, VoteForQuestion.DoesNotExist)):
#             message = 'no such user, question or vote found'
#         elif isinstance(e, PermissionError):
#             message = 'already voted'
#         else:
#             message = f'unknown exception: {e.args}'
#         return JsonResponse({'status': 'error', 'message': message}) 
    

# @transaction.atomic
# @require_POST
# @login_required
# def delete_vote(request): 
#     question_id = request.POST.get('question_id')
#     user_id = request.POST.get('user_id')

#     if not all((question_id, user_id)): 
#         return JsonResponse({'status': 'error', 
#                              'message': 'invalid input'}) 
#     try: 
#         votes_count = VoteForQuestionService.delete_existing_vote(question_id, user_id)
#         return JsonResponse({'status': 'ok', 
#                              'votes_count': votes_count}) 
#     except Exception as e: 
#         if isinstance(e, (User.DoesNotExist, Question.DoesNotExist, VoteForQuestion.DoesNotExist)):
#             message = 'no such user, question or vote found'
#         else:
#             message = f'unknown exception: {e.args}'
#         return JsonResponse({'status': 'error', 'message': message})
    

@transaction.atomic
@require_POST
@login_required 
def vote_for_question(request): 
    question_id = request.POST.get('question_id')
    user_id = request.POST.get('user_id')
    vote_type = request.POST.get('vote_type')

    if not all((question_id, user_id)): 
        return JsonResponse({'status': 'error', 
                             'message': 'invalid input'}) 
    try: 
        match vote_type: 
            case 'up': 
                votes_count = VoteForQuestionService.vote_up(question_id, user_id)
            case 'down': 
                votes_count = VoteForQuestionService.vote_down(question_id, user_id)
            case 'delete': 
                votes_count = VoteForQuestionService.delete_existing_vote(question_id, user_id)
            case _: 
                raise ValueError()
        return JsonResponse({'status': 'ok', 
                             'votes_count': votes_count}) 
    except Exception as e: 
        if isinstance(e, (User.DoesNotExist, Question.DoesNotExist, VoteForQuestion.DoesNotExist)):
            message = 'no such user, question or vote found'
        elif isinstance(e, ValueError): 
            message = 'invalid vote_type value'
        elif isinstance(e, PermissionError): 
            message = 'already voted'
        else:
            message = f'unknown exception: {e.args}'
        return JsonResponse({'status': 'error', 'message': message})