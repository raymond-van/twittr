from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import TweetForm, UserProfileForm
from .models import Tweet, Follower, UserProfile
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict

def index(request):
    username = None

    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
    else:
        return redirect('/login')

    form = TweetForm()
    following = Follower.objects.select_related().filter(follower=user)
    feed_tweets = Tweet.objects.none()

    if request.POST:
        form = TweetForm(request.POST)
        if form.is_valid():
            new_tweet = form.cleaned_data.get('tweet')
            Tweet(tweet_content=new_tweet, tweet_author=user,date_posted=timezone.now()).save()
            return HttpResponseRedirect(request.path_info)
    
    for follow in following:
        tweets = Tweet.objects.select_related().filter(tweet_author=follow.followed)
        feed_tweets = feed_tweets | tweets
    feed_tweets = feed_tweets | Tweet.objects.select_related().filter(tweet_author=user)
    feed_tweets = feed_tweets.order_by('-date_posted')

    return render(request, 'feed/feed.html', {'form':form, 'feed_tweets': feed_tweets})

def login_req(request):
    if request.POST:
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
    if request.POST:
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
    profile = User.objects.get(username=profile)
    tweets = Tweet.objects.select_related().filter(tweet_author=profile)
    following = Follower.objects.select_related().filter(follower=profile)
    followers = Follower.objects.select_related().filter(followed=profile)
    user_following_profile = followers.filter(follower=request.user)
    profile_form = UserProfileForm()

    if 'unfollow' in request.POST:
        Follower.objects.select_related().filter(follower=request.user).filter(followed=profile).delete()
        return HttpResponseRedirect(request.path_info)
    elif 'follow' in request.POST:
        Follower.objects.create(follower=request.user, followed=profile)
        return HttpResponseRedirect(request.path_info)
    elif 'add-bio' in request.POST:
        bio = request.POST['bio']
        user_profile, created = UserProfile.objects.update_or_create(user=request.user, defaults={'bio': bio})
        return HttpResponseRedirect(request.path_info)
    elif 'edit-bio' in request.POST:
        bio = request.user.profile.bio
        profile_form = UserProfileForm(initial={'bio': bio})
        UserProfile.objects.filter(user=request.user).update(bio='')
        return render(request, 'feed/profile.html', {'profile': profile, 'tweets': tweets, 'following': following, 'followers': followers, 'user_following_profile': user_following_profile, 'profile_form': profile_form})

    return render(request, 'feed/profile.html', {'profile': profile, 'tweets': tweets, 'following': following, 'followers': followers, 'user_following_profile': user_following_profile, 'profile_form': profile_form})

def tweet_delete(request, tweet_id, redirect_url):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    tweet.delete()
    if redirect_url != 'feed':
        profile = '/' + redirect_url
        return redirect(profile)
    return redirect('/')