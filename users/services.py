from datetime import timedelta
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils import timezone
from .models import User

token_generator: PasswordResetTokenGenerator

class AuthService:

    @staticmethod
    def email_exists(email: str) -> bool:
        return User.objects.filter(email=email).exists()

    @staticmethod
    def username_exists(username: str) -> bool:
        return User.objects.filter(username=username).exists()

    @staticmethod
    def register_user(username: str, email: str, raw_password: str, is_active: bool = True) -> User:
        new_user = User.objects.create(username=username, email=email)
        new_user.set_password(raw_password)
        new_user.save()
        return new_user

    @staticmethod
    def another_user_has_same_username(current_user: User) -> bool:
        return User.objects.filter(username=current_user.username).exclude(pk=current_user.pk).exists()

    @staticmethod
    def another_user_has_same_email(current_user: User) -> bool:
        return User.objects.filter(email=current_user.email).exclude(pk=current_user.pk).exists()


class UserService():
    def get_user_by_id(user_id: int) -> User | None:
        return User.objects.get(pk=user_id)
    


    

class VerifyMailingService():

    @staticmethod
    def send_email_for_verification(request, user: User) -> None:
        current_site = get_current_site(request)
        context = {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token_generator.make_token(user),
        }
        message = render_to_string( template_name='registration/verify_email.html', 
                                   context=context)
        email = EmailMessage(subject='Верификация электронной почты',
                             body=message, 
                             to=[user.email])
        email.send()



    

    