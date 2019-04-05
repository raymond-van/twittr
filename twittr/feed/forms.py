from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class TweetForm(forms.Form):
    tweet = forms.CharField(label='tweet', max_length=240, widget=forms.Textarea)
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio',)

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)
