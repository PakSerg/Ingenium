from .models import User 
from django.contrib.auth  import login, authenticate, get_user


class AuthService:

    def email_exists(email: str) -> bool:
        return User.objects.filter(email=email).exists() 
    
    def username_exists(username: str) -> bool:
        return User.objects.filter(username=username).exists() 

    def register_user(username: str, email: str, password: str) -> User: 
        new_user = User.objects.create(username=username, email=email)
        new_user.set_password(password) 
        new_user.save() 
        return new_user
    
    def another_user_has_same_username(current_user: User) -> bool: 
        return User.objects.filter(username=current_user.username).exclude(pk=current_user.pk).exists()
    
    def another_user_has_same_email(current_user: User) -> bool: 
        return User.objects.filter(email=current_user.email).exclude(pk=current_user.pk).exists()
    
    def update_username(new_username: str, current_user: User) -> None: 
        current_user.username = new_username 
        current_user.save()

