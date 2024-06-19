from datetime import timedelta
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils import timezone
from django.contrib.sites.models import Site
from .models import User


class AuthService:

    @staticmethod
    def email_exists(email: str) -> bool:
        return User.objects.filter(email=email).exists()

    @staticmethod
    def username_exists(username: str) -> bool:
        return User.objects.filter(username=username).exists()

    @staticmethod
    def register_user(username: str, email: str, raw_password: str, is_active: bool = True) -> User:
        new_user = User.objects.create(username=username, email=email, is_active=is_active)
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

    @staticmethod 
    def get_user_by_id(user_id: int) -> User | None:
        return User.objects.get(pk=user_id)
    
    @staticmethod 
    def delete_inactive_users_with_email(email: str) -> None: 
        User.objects.filter(is_active=False, email=email).delete()
    
    @staticmethod 
    def delete_all_inactive_users() -> None: 
        User.objects.filter(is_active=False).delete()


    

class VerifyMailingService():

    @staticmethod
    def send_verification_email(user_id: int) -> None:
        user = UserService.get_user_by_id(user_id)
        current_site = Site.objects.get_current()
        context = {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token_generator.make_token(user),
        }
        message = render_to_string(template_name='registration/verify_email.html', 
                                   context=context)
        email = EmailMessage(subject='Верификация электронной почты',
                             body=message, 
                             to=[user.email])
        
        email.send(fail_silently=False)

