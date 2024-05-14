from django.test import TestCase
from .models import User 
from .services import AuthService, UserService


class AuthServiceTestCase(TestCase): 

    def setUp(self):
        self.user = User.objects.create(username='test_user', 
                                        email='test@gmail.com', password='test_password')

    def test_email_exists(self): 
        email_exists = AuthService.email_exists('test@gmail.com')
        self.assertTrue(email_exists) 

    def test_username_exists(self): 
        username_exists = AuthService.username_exists('test_user') 
        self.assertTrue(username_exists) 

    def test_register_user(self): 
        AuthService.register_user(username = 'another_test', 
                                             email='another_test@gmail.com', 
                                             password='another_test_password') 
        self.assertTrue(User.objects.filter(username='another_test').exists())

    def test_another_user_has_same_username_and_email(self): 
        user = User(username='test_user', email='test@gmail.com', password='12345678') 
        self.assertTrue(AuthService.another_user_has_same_username(user)) 
        self.assertTrue(AuthService.another_user_has_same_email(user))


class UserServiceTestCase(TestCase): 
    def setUp(self):
        self.user: User = User.objects.create(username='test_user', 
                                        email='test@gmail.com', password='test_password') 
        
    def test_get_user_by_id(self): 
        user = UserService.get_user_by_id(self.user.pk) 
        self.assertEqual(user, self.user)