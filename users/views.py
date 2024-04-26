from django.shortcuts import render, redirect
from django.contrib.auth  import login, authenticate, logout, get_user
from django.contrib.auth.decorators import login_required
from django.views import View 
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import CreateUserForm, LoginForm, ProfileEditForm
from .services import AuthService
from .models import User 
from django.utils.decorators import method_decorator
    

class RegisterView(FormView):
    template_name = 'users/auth/register.html' 
    form_class = CreateUserForm 
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        cd = form.cleaned_data 

        username = cd['username'] 
        email = cd['email'] 
        password = cd['password'] 

        user = AuthService.register_user(username, email, password) 
        login(self.request, user) 
        return super().form_valid(form)
 
    
class LoginView(FormView):
    template_name = 'users/auth/login.html' 
    form_class = LoginForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form: LoginForm):
        cd = form.cleaned_data 
        user = authenticate(self.request, email=cd['email'], password=cd['password'])
        if user:
            login(self.request, user)
            print('Залогинились')
            return super().form_valid(form) 
        else:
            form.add_error(None, "Неверный логин или пароль")
            return self.form_invalid(form)
            

class LogoutView(View):
    def get(self, request):
        logout(request) 
        return redirect('users:login')


@method_decorator(login_required, name='dispatch')
class ProfileEditView(View):
    template_name = 'users/profile.html' 
    success_url = reverse_lazy('users:profile')

    def get(self, request):
        user = request.user
        profile_form = ProfileEditForm(initial={
            'username': user.username, 
            'email': user.email, 
            'image': user.image})    
        return render(request, self.template_name, {'profile_form': profile_form}) 
    
    def post(self, request):
        user = request.user

        form = ProfileEditForm(request.POST, request.FILES) 
        if form.is_valid():
            cd = form.cleaned_data
            user.username = cd['username']
            user.email = cd['email']
            user.image = cd['image']
            
            if 'image' in request.FILES:
                image_data = request.FILES['image']
                user.image = image_data

            if AuthService.another_user_has_same_email(user):
                form.add_error('email', 'Эта электронная почта уже занята')
            elif AuthService.another_user_has_same_username(user): 
                form.add_error('username', 'Это имя уже занято') 
            else: 
                user.save()
                return redirect(self.success_url) 
        return render(request, self.template_name, {'profile_form': form}) 

