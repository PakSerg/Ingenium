from django import forms 
from .models import Answer, Question


class CreateAnswerForm(forms.ModelForm): 
    class Meta:
        model = Answer 
        fields = ['content'] 
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Введите свой ответ', 'rows': 3}),
        } 
        labels = {
            'content': '',
        } 


class CreateQuestionForm(forms.ModelForm): 
    class Meta: 
        model = Question 
        fields = ['title', 'content', 'category', 'tags'] 
        labels = {
            'title': 'Название', 
            'content': 'Содержание (опционально)', 
            'category': 'Категория', 
            'tags': 'Теги (опционально)',
        }
        widgets = {
            'content': forms.Textarea(attrs={'style': 'height: 80px',})
        }


class SearchForm(forms.Form):
    query = forms.CharField(max_length=30, label='', widget=forms.TextInput(attrs={
        'placeholder': 'Найти вопрос...', 
        'class': 'form-control me-2', 
    }))