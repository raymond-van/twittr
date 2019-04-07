from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import TweetForm, UserProfileForm, ImageUploadForm
from .models import Tweet, Like, Follower, UserProfile, Reply, LikeReply
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict

def index(request):
    username = None
    user = None

    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
    else:
        return redirect('/login')

    form = TweetForm()
    following = Follower.objects.select_related().filter(follower=user)
    feed_tweets = Tweet.objects.none()

    for follow in following:
        tweets = Tweet.objects.select_related().filter(tweet_author=follow.followed)
        feed_tweets = feed_tweets | tweets
    feed_tweets = feed_tweets | Tweet.objects.select_related().filter(tweet_author=user)
    feed_tweets = feed_tweets.order_by('-date_posted')

    if 'like' in request.POST:
        tweet_content = request.POST['like']
        tweet = Tweet.objects.select_related().filter(tweet_content=tweet_content)
        new_like, created = Like.objects.get_or_create(user=user,tweet=tweet[0])
        if not created:
            Like.objects.get(user=user,tweet=tweet[0]).delete()
        return HttpResponseRedirect(request.path_info)
    elif 'reply' in request.POST:
        op_tweet_content = request.POST.get('reply')
        op_tweet = Tweet.objects.get(tweet_content=op_tweet_content)
        new_reply = request.POST['tweet']
        Reply.objects.create(op_tweet=op_tweet, user=user, date_posted=timezone.now(),reply_content=new_reply)
        return render(request, 'feed/feed.html', {'form':form, 'feed_tweets': feed_tweets, 'op_tweet_id': op_tweet.id})
    elif 'like-reply' in request.POST:
        reply_pk = request.POST['like-reply']
        reply = Reply.objects.get(pk=reply_pk)
        new_like, created = LikeReply.objects.get_or_create(user=user,reply=reply)
        op_tweet_id = reply.op_tweet.id
        if not created:
            LikeReply.objects.get(user=user,reply=reply).delete()
        return render(request, 'feed/feed.html', {'form':form, 'feed_tweets': feed_tweets, 'op_tweet_id': op_tweet_id})
    elif request.POST:
        form = TweetForm(request.POST)
        print('tweet')
        if form.is_valid():
            new_tweet = form.cleaned_data.get('tweet')
            Tweet(tweet_content=new_tweet, tweet_author=user,date_posted=timezone.now()).save()
            return HttpResponseRedirect(request.path_info)

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
    image_form = ImageUploadForm()

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
        return render(request, 'feed/profile.html', {'profile': profile, 'tweets': tweets, 'following': following, 'followers': followers, 'user_following_profile': user_following_profile, 'profile_form': profile_form, 'image_form': image_form})
    elif 'upload-pic' in request.POST:
        picture = request.POST.get('picture')
        UserProfile.objects.filter(user=request.user).update(picture=picture)
        image_form = ImageUploadForm(request.POST, request.FILES)
        return HttpResponseRedirect(request.path_info)
    elif 'like' in request.POST:
        tweet_content = request.POST['like']
        tweet = Tweet.objects.select_related().filter(tweet_content=tweet_content)
        new_like, created = Like.objects.get_or_create(user=request.user,tweet=tweet[0])
        if not created:
            Like.objects.get(user=request.user,tweet=tweet[0]).delete()
        return HttpResponseRedirect(request.path_info)

    return render(request, 'feed/profile.html', {'profile': profile, 'tweets': tweets, 'following': following, 'followers': followers, 'user_following_profile': user_following_profile, 'profile_form': profile_form, 'image_form': image_form})

def tweet_delete(request, tweet_id, redirect_url):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    tweet.delete()
    if redirect_url != 'feed':
        profile = '/' + redirect_url
        return redirect(profile)
    return redirect('/')