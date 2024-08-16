from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as django_auth_views

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve

from questions.urls import MainView, LandingView


urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', include('django.contrib.auth.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    path('', MainView.as_view(), name='main'), 

    path('welcome/', LandingView.as_view(), name='landing'), 
    path('users/', include('users.urls', namespace='users')),
    path('questions/', include('questions.urls', namespace='questions')), 
    path('votes/', include('votes.urls', namespace='votes')),

] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)