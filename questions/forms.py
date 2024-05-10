from django import forms 
from .models import Answer


class CreateAnswerForm(forms.ModelForm): 

    class Meta:
        model = Answer 
        fields = ['content'] 
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Введите свой ответ', 'rows': 3})
        } 
        labels = {
            'content': ''
        }