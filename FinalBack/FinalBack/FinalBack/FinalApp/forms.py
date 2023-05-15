from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Post, Comment


class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['photo', 'text', 'category']


class WriteComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']