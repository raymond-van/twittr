from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

def upload_to(instance, filename):
    return 'profile_pictures/%s/%s' % (instance.user.username, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=140)
    picture = models.ImageField(upload_to=upload_to, blank=True)

    def __str__(self):
        return 'Profile of user: {}'.format(self.user.username)

        
class Tweet(models.Model):
    tweet_content = models.CharField(max_length=280)
    tweet_author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField()

    def __str__(self):
        return self.tweet_content

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} liked {self.tweet}'

class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    op_tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    reply_content = models.CharField(max_length=280)
    date_posted = models.DateTimeField()
    
    def __str__(self):
        return f'{self.user} reply to {self.op_tweet}'

class LikeReply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} liked {self.reply}'


class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'm_follower')
    followed = models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'm_followed')

    def __str__(self):
        return f'{self.follower} following {self.followed}'
