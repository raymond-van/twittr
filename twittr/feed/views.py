from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import TweetForm
from .models import Tweet

def index(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.cleaned_data.get('tweet')
            return render(request, 'feed/profile.html', {'form':form})        
    form = TweetForm()
    return render(request, 'feed/feed.html', {'form':form})
    # return render(request, 'feed/base.html')

def login_req(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    form = AuthenticationForm()
    return render(request, 'feed/login.html', {'form': form})

def logout_req(request):
    logout(request)
    return redirect('/')

def register(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])
    form = UserCreationForm()
    return render(request, 'feed/register.html', {'form': form})

def profile(request, username):
    user = User.objects.get(username=username)
    tweets = Tweet.objects.select_related().filter(tweet_author=user)
    return render(request, 'feed/profile.html', {'tweets': tweets})
    # return HttpResponse("You're on profile: %s." % username)
