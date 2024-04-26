from django import forms 
from .models import User 
from .services import AuthService


class CreateUserForm(forms.ModelForm):

    class Meta:
        model = User 
        fields = ['username', 'email', 'password'] 
        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
        }
        help_texts = {
            'username': '',
        }

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput) 

    def clean_password2(self):  
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        if len(cd['password2']) < 8:
            raise forms.ValidationError('Пароль слишком короткий')
        return cd['password2'] 
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if AuthService.email_exists(email):
            raise forms.ValidationError('Пользователь с таким адресом электронной почты уже существует')
        return email 
    
    def clean_username(self): 
        username = self.cleaned_data['username'] 
        if AuthService.username_exists(username):
            raise forms.ValidationError('Пользователь с таким именем уже существует') 
        return username 
    

class LoginForm(forms.Form):
    email = forms.EmailField(label='Электронная почта', widget=forms.EmailInput)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    
    def clean_password(self):
        password = self.cleaned_data['password'] 
        if len(password) < 8:
            raise forms.ValidationError('Пароль слишком короткий') 
        return password
    

class ProfileEditForm1(forms.ModelForm): 

    class Meta:
        model = User 
        fields = ['username', 'email', 'image'] 
        labels = {
            'username': 'Имя', 
            'email': 'Электронная почта',
            'image': 'Аватар'
        }
        help_texts = {
            'username': 'Не более 30 символов'
        } 
        
    def clean_username(self): 
        username = self.cleaned_data['username'] 
        if AuthService.another_user_has_same_username(self.instance):
            raise forms.ValidationError('Это имя занято') 
        return username 
    
    def clean_email(self):
        email = self.cleaned_data['email'] 
        if AuthService.another_user_has_same_email(self.instance):
            raise forms.ValidationError('Эта электронная почта занята')
        return email 


class ProfileEditForm(forms.Form): 
    username = forms.CharField(label='Имя', help_text='Не более 30 символов') 
    email = forms.EmailField(label='Электронная почта', widget=forms.EmailInput)
    image = forms.ImageField(label='Аватар', required=False) 