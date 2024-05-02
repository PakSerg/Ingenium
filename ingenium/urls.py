from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

# from users.urls import LoginView


urlpatterns = [
    path('admin/', admin.site.urls), 
    path('users/', include('users.urls', namespace='users')),
    path('questions/', include('questions.urls', namespace='questions'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)