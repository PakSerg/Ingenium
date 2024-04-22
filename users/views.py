from django.shortcuts import render, redirect
from django.contrib.auth  import login, authenticate, logout
from django.views import View 
from django.http import HttpRequest
from .forms import CreateUserForm, LoginForm
from .services import AuthService


class Register(View): 
    template_name = 'auth/register.html' 

    def get(self, request):
        context = {
            'form': CreateUserForm()
        }
        return render(request, self.template_name, context) 
    
    def post(self, request): 
        form = CreateUserForm(request.POST) 
        if form.is_valid():
            cd = form.cleaned_data 

            username = cd['username'] 
            email = cd['email'] 
            password = cd['password'] 

            user = AuthService.register_user(username, email, password) 
            login(request, user)

            return redirect('users:test')  
        
        context = {
            'form': form
        }
        return render(request, self.template_name, context)
 

class Login(View):
    template_name = 'auth/login.html' 

    def get(self, request):
        context = {
            'form': LoginForm(),
        } 
        return render(request, self.template_name, context) 
    
    def post(self, request): 
        form = LoginForm(request.POST) 

        if form.is_valid():
            cd = form.cleaned_data 
            email = cd['email'] 
            password = cd['password']
            
            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)
                print('Залогинились')
                return redirect('users:test')  
            
        form.add_error(None, 'Неверный адрес электронной почты или пароль')
            
        context = {
            'form': form
        }
        return render(request, self.template_name, context)
            

class Logout(View):
    def get(self, request):
        logout(request) 
        return redirect('users:test')


class Test(View):
    def get(self, request):
        return render(request, 'test.html')