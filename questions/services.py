from django.db.models.query import QuerySet, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import TrigramSimilarity
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.models import Site
from django.db.models import Count
from .models import Question, Category, Answer, Tag 
from users.models import User
from users.services import UserService


class QuestionService: 
    @staticmethod
    def get_question_by_id(question_id: int) -> Question: 
        return Question.objects.get(pk=question_id)
    
    @staticmethod 
    def create_and_publish_question(title: str, 
                        category: Category, 
                        user: User, 
                        content: str = None, 
                        tags: QuerySet[Tag] = None) -> Question: 
        new_question = Question(title=title, 
                                category=category, 
                                user=user,
                                content=content, 
                                status=Question.Status.PUBLISHED)
        new_question.save()
        new_question.tags.set(tags)
        return new_question
    
    @staticmethod
    def get_published_questions_sorted_by_votes(count: int = None) -> QuerySet[Question]: 
        questions = Question.published.order_by('-votes_count')
        return questions if count == None else questions[:count]
    
    @staticmethod 
    def get_published_questions_for_category(category: Category, count: int = None) -> QuerySet[Question]: 
        questions = Question.published.filter(category=category).order_by('-votes_count')
        return questions if count == None else questions[:count]
    
    @staticmethod 
    def get_published_questions_with_tag(tag: Tag, count: int = None) -> QuerySet[Question]: 
        questions = Question.published.filter(tags=tag).order_by('-votes_count')
        return questions if count == None else questions[:count]
    
    @staticmethod 
    def get_similar_questions(current_question: Question, count: int = 4) -> QuerySet[Question]: 
        question_tags_ids = current_question.tags.values_list('id', flat=True)  
        similar_questions = Question.published.filter(tags__in=question_tags_ids).exclude(id=current_question.id) 
        similar_questions = similar_questions.annotate(same_tags=Count('tags')).order_by('-same_tags', '-created_at', 'votes_count')
        return similar_questions[:count]
    
    @staticmethod 
    def get_published_question(year: int, month: int, day: int, question_slug: str) -> Question | None: 
        return Question.published.filter(created_at__year=year, 
                                       created_at__month=month, 
                                       created_at__day=day, 
                                       slug=question_slug).first()


class CategoryService: 
    @staticmethod 
    def get_all_categories() -> QuerySet[Category]: 
        categories = Category.objects.all() 
        return categories
    
    @staticmethod 
    def get_category_by_slug(slug: str) -> Category: 
        return Category.objects.get(slug=slug)
    

class TagService: 
    @staticmethod 
    def get_tag_by_slug(slug: str) -> Tag: 
        return Tag.objects.get(slug=slug)
    

class SearchService: 
    @staticmethod 
    def search_questions_by_query(query: str) -> QuerySet[Question]:
        results = Question.published.annotate(
            title_similarity=TrigramSimilarity('title', query),
            content_similarity=TrigramSimilarity('content', query)
        ).filter(
            Q(title_similarity__gt=0.1) | Q(content_similarity__gt=0.1)
        ).order_by(
            '-title_similarity', '-content_similarity'
        )

        return results
    

class AnswerService: 
    @staticmethod 
    def create_answer(content: str, user: User, question: Question) -> Answer: 
        new_answer = Answer.objects.create(content=content, user=user, question=question)
        new_answer.save()
        return new_answer
    

class NotificationService: 
    @staticmethod 
    def send_new_answer_notification(recipient_user_id: int, question_id: int) -> None:
        user = UserService.get_user_by_id(recipient_user_id)
        question = QuestionService.get_question_by_id(question_id)
        current_site = Site.objects.get_current()
        context = {
            'domain': current_site.domain,
            'user': user,
            'question': question
        }
        message = render_to_string(template_name='questions/new_answer_email.html', 
                                   context=context)
        email = EmailMessage(subject='Новый ответ на ваш вопрос',
                             body=message, 
                             to=[user.email])
        email.content_subtype = 'html'
        email.send(fail_silently=False)


def get_paginated_collection(request, collection: QuerySet, count_per_page: int = 10): 
    paginator = Paginator(collection, count_per_page)
    page_number = request.GET.get('page', 1)
    try:
        collection = paginator.page(page_number)
    except PageNotAnInteger:
        collection = paginator.page(1)
    except EmptyPage:
        collection = paginator.page(paginator.num_pages) 
    return collection