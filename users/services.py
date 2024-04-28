from .models import User 


class AuthService:

    @staticmethod
    def email_exists(email: str) -> bool:
        return User.objects.filter(email=email).exists() 
    
    @staticmethod
    def username_exists(username: str) -> bool:
        return User.objects.filter(username=username).exists() 

    @staticmethod
    def register_user(username: str, email: str, password: str) -> User: 
        new_user = User.objects.create(username=username, email=email)
        new_user.set_password(password) 
        new_user.save() 
        return new_user
    
    @staticmethod
    def another_user_has_same_username(current_user: User) -> bool: 
        print(f'{current_user=}')
        return User.objects.filter(username=current_user.username).exclude(pk=current_user.pk).exists()
    
    @staticmethod
    def another_user_has_same_email(current_user: User) -> bool: 
        return User.objects.filter(email=current_user.email).exclude(pk=current_user.pk).exists()
    


