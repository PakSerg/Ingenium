from django.shortcuts import render
from django.views import View 
from django.urls import reverse_lazy, reverse
from .services import QuestionService, CategoryService


class AllQuestionsView(View): 
    template_name = 'questions/all_questions.html'

    def get(self, request): 
        questions = QuestionService.get_published_sorted_by_votes() 
        context = {
            'questions': questions,
        }
        return render(request, self.template_name, context) 


class AllCategoriesView(View): 
    template_name = ... 

    def get(self, request): 
        ...

class SingleQuestionView(View): 
    template_name = 'questions/single_question.html'

    def get(self, request, year: int, month: int, day: int, question_slug: str): 
        question = QuestionService.get_published_by_slug_and_datetime(year, month, day, question_slug)
        context = {'question': question} 
        return render(request, self.template_name, context) 


class CategoryView(View): 
    template_name = 'questions/questions_in_category.html' 

    def get(self, request, category_slug: str): 
        category = CategoryService.get_by_slug(category_slug)
        questions = QuestionService.get_published_in_category(category_slug)
        context = {
            'questions': questions, 
            'category': category,
        }
        return render(request, self.template_name, context) 


class TagView(View): 
    ...