from django.db.models.query import QuerySet
from .models import Question, Category, Answer 
from users.models import User


class QuestionService: 

    @staticmethod
    def get_published_sorted_by_votes(count: int = None) -> QuerySet[Question] | None: 
        questions = Question.published.order_by('votes')
        if count:
            questions = questions[:count]
        return questions 
    
    @staticmethod 
    def get_published_in_category(category_slug: str, count: int = None) -> QuerySet[Question] | None: 
        questions = Question.published.filter(category=CategoryService.get_by_slug(category_slug))
        return questions
    
    @staticmethod 
    def get_published_by_datetime_and_slug(year: int, month: int, day: int, question_slug: str) -> Question | None: 
        return Question.published.filter(created_at__year=year, 
                                       created_at__month=month, 
                                       created_at__day=day, 
                                       slug=question_slug).first()

class CategoryService: 
    
    @staticmethod 
    def get_all_categories() -> QuerySet[Category] | None: 
        categories = Category.objects.all() 
        return categories
    
    @staticmethod 
    def get_by_slug(slug: str) -> Category | None: 
        return Category.objects.filter(slug=slug).first() 
    

class AnswerService: 

    @staticmethod 
    def create_answer(content: str, user: User, question: Question) -> Answer: 
        new_answer = Answer.objects.create(content=content, user=user, question=question)
        new_answer.save()
        return new_answer