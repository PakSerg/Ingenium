from django.shortcuts import render
from django.views import View 
from django.urls import reverse_lazy, reverse
from .services import QuestionService, CategoryService


class SingleQuestionView(View): 
    ...


class AllQuestionsView(View): 
    template_name = 'questions/all_questions.html'

    def get(self, request): 
        questions = QuestionService.get_published_questions_sorted_by_votes() 
        categories = CategoryService.get_all_categories()
        context = {
            'questions': questions,
            'categories': categories,
        }
        return render(request, self.template_name, context) 


class CategoryView(View): 
    ...


class TagView(View): 
    ...