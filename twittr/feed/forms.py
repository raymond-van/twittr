from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class TweetForm(forms.Form):
    tweet = forms.CharField(label='', max_length=240, widget=forms.Textarea(attrs={'placeholder': 'What\'s happening?', 'class': 'tweet-field','cols': 30}))
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio',)
        labels = {
            'bio': '',
        }

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)
