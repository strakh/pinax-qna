from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

class Profile(models.Model):
    """A user using the Quanda system. This can be an anonymous user."""
    user = models.OneToOneField(User, verbose_name=_('user'))
    name = models.CharField(_('name'), max_length=50, null=True, blank=True)
    reputation = models.IntegerField(default=0)
    bio = models.TextField(_('bio'),blank=True)
    location = models.CharField(_('location'), max_length=140, blank=True)
    website = models.URLField(_('website'), null=True, blank=True, verify_exists=False)
    
    def __unicode__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return ('profile_detail', None, {'username': self.user.username})
    get_absolute_url = models.permalink(get_absolute_url)
    
    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

def create_profile(sender, instance=None, **kwargs):
    if instance is None:
        return
    profile, created = Profile.objects.get_or_create(user=instance)

post_save.connect(create_profile, sender=User)

