from django.urls import path, include
from .views import *


app_name = 'users'

urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(), name='register'), 
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('test/', Test.as_view(), name='test'),
]