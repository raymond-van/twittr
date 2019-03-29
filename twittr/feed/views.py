from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import TweetForm
from .models import Tweet, Follower
from django.utils import timezone

def index(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            new_tweet = form.cleaned_data.get('tweet')
            Tweet(tweet_content=new_tweet, tweet_author=user,date_posted=timezone.now()).save()
            tweets = Tweet.objects.select_related().filter(tweet_author=user)
            following = Follower.objects.select_related().filter(follower=user)
            followers = Follower.objects.select_related().filter(followed=user)
            return render(request, 'feed/profile.html', {'user': user, 'tweets': tweets, 'following': following, 'followers': followers})
    form = TweetForm()
    return render(request, 'feed/feed.html', {'form':form})

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

def profile(request, profile):
    # user = None
    # if request.user.is_authenticated:
    #     user = request.user
    profile = User.objects.get(username=profile)
    tweets = Tweet.objects.select_related().filter(tweet_author=profile)
    following = Follower.objects.select_related().filter(follower=profile)
    followers = Follower.objects.select_related().filter(followed=profile)
    return render(request, 'feed/profile.html', {'profile': profile, 'tweets': tweets, 'following': following, 'followers': followers})
