import os

from django.conf import settings
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from .forms import CreateUser, WriteComment, CreatePost
from .models import Post, Comment


# Create your views here.


def LogoutUser(request):
    logout(request);
    return redirect('TrainerSite')


def Trainer(request):
    posts = Post.objects.all()
    if request.user.is_authenticated:
        username = request.user.username
        email = request.user.email
        first_name = request.user.first_name
        last_name = request.user.last_name
        user = request.user

        context = {
            'user': user,
            'username': username,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'posts': posts

        }
    else:
        context = {
            'user': None,
            'posts': posts
        }
    return render(request, 'TrainerSite.html', context)


def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('TrainerSite')
        else:
            error_message = 'Invalid login credentials'
            return render(request, 'login.html', {'user': None, 'error_message': error_message})

    return render(request, 'login.html', {'user': None})


def register(request):
    form = CreateUser()
    if request.method == "POST":
        form = CreateUser(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('TrainerSite')

    context = {
        'form': form
    }
    return render(request, 'register.html', context)


@login_required
def PostCreation(request):
    form = CreatePost()
    if request.method == 'POST':
        form = CreatePost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('TrainerSite')
    return render(request, 'CreatePost.html', {'form': form})


def PostView(request):
    pk = request.GET.get('pk', None)
    post = Post.objects.get(id=pk)
    Comments = Comment.objects.filter(post=post)
    form = WriteComment()
    if request.method == 'POST':
        form = WriteComment(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            comment = WriteComment()
            form = WriteComment()
    return render(request, 'PostView.html', {'form': form, 'post': post, 'comments': Comments})


def search_results(request):
    query = request.GET.get('query')
    posts = Post.objects.filter(
        Q(category__icontains=query) | Q(text__icontains=query)
    )
    return render(request, 'SearchResult.html', {'posts': posts})

