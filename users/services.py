from .models import User 
from django.contrib.auth  import login, authenticate


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

    # def authenticate_user(email: str, password: str) -> User: #TODO Метод не работает, т.к. в функции не передаётся request
    #     user = authenticate(email=email, password=password)   #TODO Или надо будет придумать, как обойтись без этого, или переписать с объектом request
    #     if user is not None:
    #         login(user)
    #         return user
    #     else:
    #         return None
