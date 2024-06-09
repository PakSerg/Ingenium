from django.forms import ValidationError
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.db import transaction
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator as token_generator
from .forms import CreateUserForm, LoginForm, ProfileEditForm, PasswordChangeForm
from .services import AuthService, UserService
from .models import User
from .tasks import send_verification_email_task


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('users:verify_email_done')

    @transaction.atomic
    def form_valid(self, form):
        cd = form.cleaned_data
        username = cd['username']
        email = cd['email']
        password = cd['password']

        user = AuthService.register_user(username, email, password, is_active=False) 
        send_verification_email_task.delay(user.pk)

        return super().form_valid(form)
    

class VerifyEmailDoneView(TemplateView): 
    template_name = 'registration/verify_email_done.html'


class InvalidVerificationView(TemplateView): 
    template_name = 'registration/invalid_verification.html'


class VerifyEmailView(View): 
    def get(self, request, uidb64: str, token: str): 
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('questions:all_questions')
        return redirect('users:invalid_verification')

    @staticmethod
    def get_user(uidb64: str) -> User | None:
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = UserService.get_user_by_id(uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return user


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