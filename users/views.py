from django.shortcuts import redirect
from django.contrib.auth  import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views import View 
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.db import transaction
from .forms import CreateUserForm, LoginForm, ProfileEditForm
from .services import AuthService
from .models import User 
    

class RegisterView(FormView):
    template_name = 'users/auth/register.html' 
    form_class = CreateUserForm 
    success_url = reverse_lazy('users:profile')

    @transaction.atomic
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

    @transaction.atomic
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
class ProfileEditView(FormView):
    template_name = 'users/profile.html' 
    success_url = reverse_lazy('users:profile')
    form_class = ProfileEditForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    @transaction.atomic
    def form_valid(self, form: ProfileEditForm): 
        user: User = self.request.user
        cd = form.cleaned_data
        user.username = cd['username']
        user.email = cd['email']

        if cd.get('description'):
            user.description = cd['description']
        
        if 'image' in self.request.FILES:
            image_data = self.request.FILES['image']
            user.image = image_data

        user.save()


        return super().form_valid(form)
    


