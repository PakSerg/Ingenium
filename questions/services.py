from django.db.models.query import QuerySet
from .models import Question, Category, Answer, Tag 
from users.models import User


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

        if count:
            questions = questions[:count]
        return questions 
    
    @staticmethod 
    def get_published_questions_for_category(category_slug: str, count: int = None) -> QuerySet[Question]: 
        questions = Question.published.filter(category=CategoryService.get_category_by_slug(category_slug))
        return questions
    
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
    

class AnswerService: 
    @staticmethod 
    def create_answer(content: str, user: User, question: Question) -> Answer: 
        new_answer = Answer.objects.create(content=content, user=user, question=question)
        new_answer.save()
        return new_answer
    