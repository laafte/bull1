from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from members.views import ProfileCreateView


def completion_check(member):
    return not member.has_completed_profile


class ProfileCompletionMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path_info == reverse('members:create_profile') \
           and request.user.has_completed_profile:
            return HttpResponseRedirect(reverse('home'))
        if (not request.user.is_authenticated()) or \
           request.user.has_completed_profile or \
           request.path_info.startswith('/media/') or request.path_info.startswith('/static/'):
            return view_func(request, *view_args, **view_kwargs)
        if request.path_info == reverse('members:create_profile') and not request.user.has_completed_profile:
            return ProfileCreateView.as_view()(request, *view_args, **view_kwargs)
        else:
            return HttpResponseRedirect(reverse('members:create_profile'))