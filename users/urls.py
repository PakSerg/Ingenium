from django.urls import path, include
from django.contrib.auth import views as django_auth_views
from .views import *


app_name = 'users'

urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('register/', RegisterView.as_view(), name='register'), 
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),


    # path('', include('django.contrib.auth.urls')),

    # path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    # сброс пароля
	# path('password-reset/', django_auth_views.PasswordResetView.as_view(), name='password_reset'),
	# path('password-reset/done/', django_auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
	# path('password-reset/<uidb64>/<token>/', django_auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	# path('password-reset/complete/', django_auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('profile/', ProfileEditView.as_view(), name='profile'),
]