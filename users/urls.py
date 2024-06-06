from django.urls import path, include
from .views import *


app_name = 'users'

urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('register/', RegisterView.as_view(), name='register'), 
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('verify-email/done/', VerifyEmailDoneView.as_view(), name='verify_email_done'),
    path('invalid-verification/', InvalidVerificationView.as_view(), name='invalid_verification'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('profile/', ProfileEditView.as_view(), name='profile'),
]