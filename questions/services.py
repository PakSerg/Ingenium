from django.db.models.query import QuerySet
from .models import Question, Category, Answer 
from users.models import User


class QuestionService: 
    @staticmethod
    def get_published_questions_sorted_by_votes(count: int = None) -> QuerySet[Question]: 
        questions = Question.published.order_by('votes')
        if count:
            questions = questions[:count]
        return questions 
    
    @staticmethod 
    def get_published_questions_for_category(category_slug: str, count: int = None) -> QuerySet[Question]: 
        questions = Question.published.filter(category=CategoryService.get_by_slug(category_slug))
        return questions
    
    @staticmethod 
    def get_published_question(year: int, month: int, day: int, question_slug: str) -> Question | None: 
        return Question.published.filter(created_at__year=year, 
                                       created_at__month=month, 
                                       created_at__day=day, 
                                       slug=question_slug).first()
    
    @staticmethod 
    def set_votes_count(question_id: int, votes_count: int) -> None: 
        
        question = QuestionService.get_question_by_id(question_id)
        question.votes_count = votes_count 
        question.save() 

    @staticmethod
    def increment_votes_count(question_id: int) -> int: 
        question = QuestionService.get_question_by_id(question_id)
        
        question.votes_count += 1
        question.save()

        return question.votes_count
    
    @staticmethod
    def decrement_votes_count(question_id: int) -> int: 
        question = QuestionService.get_question_by_id(question_id)
        
        question.votes_count -= 1
        question.save()

        return question.votes_count
    
    @staticmethod
    def get_question_by_id(question_id: int) -> Question: 
        return Question.objects.get(pk=question_id)


class CategoryService: 
    @staticmethod 
    def get_all_categories() -> QuerySet[Category]: 
        categories = Category.objects.all() 
        return categories
    
    @staticmethod 
    def get_by_slug(slug: str) -> Category: 
        return Category.objects.get(slug=slug)
    

class AnswerService: 
    @staticmethod 
    def create_answer(content: str, user: User, question: Question) -> Answer: 
        new_answer = Answer.objects.create(content=content, user=user, question=question)
        new_answer.save()
        return new_answer
    