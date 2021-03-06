from django.core.urlresolvers import reverse
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from profile.models import Profile
from profile.forms import ProfileForm, RepForm

TINY_MCE_JS_LOCATION = getattr(settings, 'TINY_MCE_JS_LOCATION', 'http://teebes.com/static/js/tiny_mce/tiny_mce.js')

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None


def profiles(request, template_name="profile/profiles.html"):
    users = User.objects.all().order_by("-date_joined")
    search_terms = request.GET.get('search', '')
    order = request.GET.get('order')
    if not order:
        order = 'date'
    if search_terms:
        users = users.filter(username__icontains=search_terms)
    if order == 'date':
        users = users.order_by("-date_joined")
    elif order == 'name':
        users = users.order_by("username")
    return render_to_response(template_name, {
        'users':users,
        'order' : order,
        'search_terms' : search_terms
    }, context_instance=RequestContext(request))


def profile(request, username, template_name="profile/profile.html"):
    
    other_user = get_object_or_404(User, username=username)
    
    if request.user.is_authenticated():
        if request.user == other_user:
            is_me = True
        else:
            is_me = False
    else:
        is_me = False
    
    return render_to_response(template_name, {
        "is_me": is_me,
        "other_user": other_user,
    }, context_instance=RequestContext(request))


@login_required
def profile_edit(request, **kwargs):
    
    template_name = kwargs.get("template_name", "profile/profile_edit.html")
    
    if request.is_ajax():
        template_name = kwargs.get(
            "template_name_facebox",
            "profile/profile_edit_facebox.html"
        )
    
    profile = request.user.get_profile()
    
    if request.method == "POST":
        if request.POST.has_key('change_rep'):
            if not request.user.is_staff:
                return HttpRepsonse("Unauthorized")
            rep_form = RepForm(request.POST)
            if rep_form.is_valid():
                profile.reputation = rep_form.cleaned_data['base_rep']
                profile.save()
                return HttpResponseRedirect(reverse("profile_detail", args=[request.user.username]))
        else:
            if not request.user == profile.user:
                return HttpResponse("Unauthorized")
            profile_form = ProfileForm(request.POST, instance=profile)
            if profile_form.is_valid():
                profile = profile_form.save()
                return HttpResponseRedirect(reverse("profile_detail", args=[request.user.username]))

    else:
        profile_form = ProfileForm(instance=profile)
        rep_form = RepForm(initial={'base_rep': profile.reputation})
    
    return render_to_response(template_name, {
        "profile": profile,
        "profile_form": profile_form,
        "rep_form": rep_form,
        'tinymce': TINY_MCE_JS_LOCATION,
    }, context_instance=RequestContext(request))
