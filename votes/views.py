from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .services import VoteForQuestionService
from users.models import User
from questions.models import Question
from .models import VoteForQuestion
from django.db import transaction

@transaction.atomic
@require_POST
@login_required
def vote_up_for_question(request):
    question_id = request.POST.get('question_id')
    user_id = request.user.id

    if not question_id:
        return JsonResponse({'status': 'error', 'message': 'invalid input'})

    try:
        votes_count = VoteForQuestionService.vote_up(question_id, user_id)

        return JsonResponse({'status': 'ok', 'votes_count': votes_count})
    except Exception as e:
        if isinstance(e, (User.DoesNotExist, Question.DoesNotExist, VoteForQuestion.DoesNotExist)):
            message = 'no such user, question or vote found'
        elif isinstance(e, PermissionError):
            message = 'already voted'
        else:
            message = f'unknown exception: {e.args}'
        return JsonResponse({'status': 'error', 'message': message})

@transaction.atomic
@require_POST
@login_required
def vote_down_for_question(request):
    question_id = request.POST.get('question_id')
    user_id = request.user.id

    if not question_id:
        return JsonResponse({'status': 'error', 'message': 'invalid input'})

    try:
        votes_count = VoteForQuestionService.vote_down(question_id, user_id)

        return JsonResponse({'status': 'ok', 'votes_count': votes_count})
    except Exception as e:
        if isinstance(e, (User.DoesNotExist, Question.DoesNotExist, VoteForQuestion.DoesNotExist)):
            message = 'no such user, question or vote found'
        elif isinstance(e, PermissionError):
            message = 'already voted'
        else:
            message = f'unknown exception: {e.args}'
        return JsonResponse({'status': 'error', 'message': message})

@transaction.atomic
@require_POST
@login_required
def delete_vote_for_question(request):
    question_id = request.POST.get('question_id')
    user_id = request.user.id

    if not question_id:
        return JsonResponse({'status': 'error', 'message': 'invalid input'})

    try:
        votes_count = VoteForQuestionService.delete_existing_vote(question_id, user_id)

        return JsonResponse({'status': 'ok', 'votes_count': votes_count})
    except Exception as e:
        if isinstance(e, (User.DoesNotExist, Question.DoesNotExist, VoteForQuestion.DoesNotExist)):
            message = 'no such user, question or vote found'
        else:
            message = f'unknown exception: {e.args}'
        return JsonResponse({'status': 'error', 'message': message})
