from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.generic import TemplateView, FormView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .services import QuestionService, CategoryService, AnswerService
from votes.services import VoteForQuestionService
from .forms import CreateAnswerForm, CreateQuestionForm
from .models import Tag


class AllQuestionsView(View): 
    template_name = 'questions/all_questions.html'

    def get(self, request): 
        questions = QuestionService.get_published_questions_sorted_by_votes() 
        context = {
            'questions': questions,
        }
        return render(request, self.template_name, context) 


class AllCategoriesView(TemplateView): 
    template_name = 'questions/all_categories.html'

    def get_context_data(self):
        all_categories = CategoryService.get_all_categories()
        context = { 'categories': all_categories }
        return context
    

class SingleQuestionView(View):  
    template_name = 'questions/single_question.html'
    form_class = CreateAnswerForm

    def get(self, request, year: int, month: int, day: int, question_slug: str): 
        question = QuestionService.get_published_question(year, month, day, question_slug)
        form = CreateAnswerForm()

        user_vote = None
        if request.user.is_authenticated:
            user_vote = VoteForQuestionService.get_vote_or_none(question.pk, request.user.pk)

        context = {
            'question': question,
            'form': form, 
            'user_vote': user_vote
        } 

        return render(request, self.template_name, context) 
    
    def post(self, request, year: int, month: int, day: int, question_slug: str): 
        user = request.user 
        question = QuestionService.get_published_question(year, month, day, question_slug) 
        form = CreateAnswerForm(request.POST)

        if form.is_valid(): 
            answer_content = form.cleaned_data['content'] 
            AnswerService.create_answer(answer_content, user, question) 
            return redirect('questions:single_question', 
                            year=question.created_at.year,
                            month=question.created_at.month, 
                            day=question.created_at.day, 
                            question_slug=question.slug)
        context = {
            'question': question,
            'form': form,
        }
        return render(request, self.template_name, context) 
    

@method_decorator(login_required, name='dispatch')
class CreateQuestionView(FormView): 
    template_name = 'questions/create_question.html' 
    form_class = CreateQuestionForm

    def form_valid(self, form: CreateQuestionForm) -> HttpResponse:
        cd = form.cleaned_data
        title = cd['title']
        content = cd['content']
        category = cd['category'] 
        tags = cd['tags']

        user = self.request.user

        QuestionService.create_and_publish_question(title, category, user, content, tags)

        return redirect('questions:all_questions')
    

class CategoryView(View): 
    template_name = 'questions/questions_in_category.html' 

    def get(self, request, category_slug: str): 
        category = CategoryService.get_category_by_slug(category_slug)
        questions = QuestionService.get_published_questions_for_category(category_slug)
        context = {
            'questions': questions, 
            'category': category,
        }
        return render(request, self.template_name, context)  
    

class TagView(View): 
    ...


def get_tags(request, category_id: int) -> JsonResponse:
    tags = Tag.objects.filter(category_id=category_id).values('id', 'text')
    return JsonResponse(list(tags), safe=False)