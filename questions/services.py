from django.db.models.query import QuerySet
from .models import Question, Category


class QuestionService: 

    @staticmethod
    def get_published_questions_sorted_by_votes(count: int = None) -> QuerySet[Question] | None: 
        questions = Question.published.order_by('votes') 
        if count:
            questions = questions[:count]
        return questions 
    

class CategoryService: 

    @staticmethod 
    def get_all_categories() -> QuerySet[Category] | None: 
        categories = Category.objects.all() 
        return categories