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
        return f'{self.follower} is following {self.followed}'

    # user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user', on_delete=models.CASCADE)
    # following = models.ManyToManyField('self', related_name='follower', symmetrical=False, blank=True, null=True)
    # following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='follower', on_delete=models.CASCADE)
    # follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    
    
    
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # name = models.CharField(max_length=100, blank=True)
    # following = models.ManyToManyField('self', related_name='followers', symmetrical=False, blank=True, null=True)

    # def __unicode__(self):
    #     return self.name



# class Follower(models.Model):
#     follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='who_following', on_delete=models.CASCADE)
#     following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='who_followers', on_delete=models.CASCADE)
    
#     # class Meta:
#     #     unique_together = ('follower', 'following')

#     def __unicode__(self):
#         return u'%s follows %s' % (self.follower, self.following)

# User.add_to_class('is_following', models.ManyToOneRel('self', to=Follower, field_name='is_follower'))

# User.add_to_class('relationships', models.ManyToManyField('self', through='Relationship', symmetrical=False, related_name='related_to'))

