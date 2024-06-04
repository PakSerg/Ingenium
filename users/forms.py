from django import forms 
from .models import User 
from .services import AuthService

 
class CreateUserForm(forms.ModelForm):

    class Meta: 
        model = User 
        fields = ['username', 'email'] 
        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Введите ваше имя'}), 
            'email': forms.EmailInput(attrs={'placeholder': 'Ваша электронная почта'}), 
            'password': forms.PasswordInput(attrs={'placeholder': 'Придумайте надёжный пароль'})
        }
        help_texts = {
            'username': ''
        }

    password = forms.CharField(label='Пароль', min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'Придумайте пароль (не менее 8 символов)'}))
    password2 = forms.CharField(label='', min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'})) 
    
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
    email = forms.EmailField(label='Электронная почта', widget=forms.EmailInput(attrs={'placeholder': 'Введите электронную почту'}))
    password = forms.CharField(min_length=8, label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))


class ProfileEditForm(forms.Form): 
    username = forms.CharField(label='Имя', help_text='Не более 30 символов') 
    email = forms.EmailField(label='Электронная почта', widget=forms.EmailInput)
    image = forms.ImageField(label='Аватар', required=False) 
    description = forms.CharField(label='Немного о себе', required=False)

    def __init__(self, *args, **kwargs):
        self.user: User = kwargs.pop('user', None)
        initial = kwargs.pop('initial', {})

        initial['username'] = self.user.username
        initial['email'] = self.user.email
        initial['image'] = self.user.image
        initial['description'] = self.user.description

        kwargs['initial'] = initial
        super(ProfileEditForm, self).__init__(*args, **kwargs)

    def clean_username(self): 
        new_username = self.cleaned_data['username']
        self.user.username = new_username
        if AuthService.another_user_has_same_username(self.user):
            raise forms.ValidationError('Это имя уже занято') 
        return new_username
    
    def clean_email(self): 
        new_email = self.cleaned_data['email']
        if AuthService.another_user_has_same_email(self.user):
            raise forms.ValidationError('Эта электронная почта уже занята') 
        return new_email
    

class PasswordChangeForm(forms.Form): 
    old_password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'Введите старый пароль'}), label='Старый пароль')
    new_password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'Придумайте новый пароль'}), label='Новый пароль')
    new_password_confirmation = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердите новый пароль'}), label='')

    def __init__(self, *args, **kwargs): 
        self.user: User = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_new_password_confirmation(self): 
        new_password = self.cleaned_data['new_password'] 
        new_password_confirmation = self.cleaned_data['new_password_confirmation'] 

        if new_password != new_password_confirmation: 
            raise forms.ValidationError('Пароли не совпадают') 
        return new_password_confirmation
    
    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if not self.user.check_password(old_password): 
            raise forms.ValidationError('Неверный пароль')
        return old_password
    
    def save(self) -> User: 
        new_password = self.cleaned_data['new_password']
        self.user.set_password(new_password)
        self.user.save()
        return self.user