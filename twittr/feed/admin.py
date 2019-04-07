from django.contrib import admin
from .models import Tweet, Follower, UserProfile, Like, LikeReply, Reply

admin.site.register(Tweet)
admin.site.register(Follower)
admin.site.register(UserProfile)
admin.site.register(Like)
admin.site.register(LikeReply)
admin.site.register(Reply)