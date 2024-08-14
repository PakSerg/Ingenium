from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as django_auth_views

from questions.urls import AllQuestionsView


urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', include('django.contrib.auth.urls')),
    path('__debug__/', include('debug_toolbar.urls')),

    path('users/', include('users.urls', namespace='users')),
    path('questions/', include('questions.urls', namespace='questions')), 
    path('votes/', include('votes.urls', namespace='votes')),

    path('', AllQuestionsView.as_view()), 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)