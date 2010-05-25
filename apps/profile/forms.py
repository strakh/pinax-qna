from django.conf import settings
from django import forms

from profile.models import Profile
from quanda.utils import strip_js
#from profile.models import Profile

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ('user',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'reputation']
    
#    def __init__(self, user, *args, **kwargs):
#        super(ProfileForm, self).__init__(*args, **kwargs)
#        self.user = user
#    
    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        profile = super(ProfileForm, self).save(*args, **kwargs)
        profile.bio = strip_js(profile.bio)
#        profile.user = self.user
        profile.save()
        return profile

class RepForm(forms.Form):
    base_rep = forms.IntegerField()
    #username = forms.CharField(max_length=140, widget=forms.HiddenInput, required=True)

