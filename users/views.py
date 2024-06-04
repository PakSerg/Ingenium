from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.db import transaction
from django.core.mail import send_mail
from .forms import CreateUserForm, LoginForm, ProfileEditForm, PasswordChangeForm
from .services import AuthService
from .models import User


class RegisterView(FormView):
    template_name = 'registration/register.html'
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
    template_name = 'registration/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('questions:all_questions')

    @transaction.atomic
    def form_valid(self, form: LoginForm):
        cd = form.cleaned_data
        email = cd['email']
        password = cd['password']
        user = authenticate(self.request, email=email, password=password)
        if user:
            login(self.request, user)
            return super().form_valid(form)

        form.add_error(None, "Неверный логин или пароль")
        return self.form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('questions:all_questions')


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


@method_decorator(login_required, name='dispatch')
class PasswordChangeView(FormView):
    template_name = 'registration/password_change.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('users:profile')

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['user'] = self.request.user
        return form_kwargs

    def form_valid(self, form):
        self.request.user = form.save()
        update_session_auth_hash(self.request, self.request.user)
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class PasswordResetView(TemplateView):
    template_name = 'registration/password_reset_form.html'

    def get(self, request, *args, **kwargs):

        return super().get(request, *args, **kwargs)
