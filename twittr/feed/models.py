from django.db import models
from django.contrib.auth.models import User
# from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Tweet(models.Model):
    tweet_content = models.CharField(max_length=240)
    tweet_author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField()

    def __str__(self):
        return self.tweet_content


class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'm_follower')
    followed = models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'm_followed')

    def __str__(self):
        return f'{self.follower} following {self.followed}'
        