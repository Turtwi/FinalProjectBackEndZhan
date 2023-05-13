from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.Trainer, name='TrainerSite'),
    path('Login', views.loginUser, name='Login'),
    path('Logout', views.LogoutUser, name='Logout'),
    path('Register', views.register, name='Register'),
    path('CreatePost', views.PostCreation, name='PostCreation'),
    path('PostView', views.PostView, name='PostView')

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)