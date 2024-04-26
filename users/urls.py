from django.urls import path, include
from .views import *


app_name = 'users'

urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('register/', RegisterView.as_view(), name='register'), 
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileEditView.as_view(), name='profile'),
]