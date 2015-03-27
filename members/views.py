from __future__ import division
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout as auth_logout

# Create your views here.
from django.views.generic import TemplateView
from social_auth.db.django_models import UserSocialAuth
from libs.instagram.tools import InstagramSession

from .models import Member


class MemberHomePageView(TemplateView):
    """
    Member home page
    """

    template_name = 'members/index.html'

    def get(self, request, *args, **kwargs):
        '''Serve GET request'''

        self.template_name = 'members/index.html'

        return render(request, self.template_name,
                      dict(request=request, )
        )


class MemberWelcomeView(TemplateView):
    template_name = 'members/welcome.html'

    def get(self, request, *args, **kwargs):
        return render(request,
                      self.template_name,
                      dict(
                      )
        )


class MemberDashboardView(TemplateView):
    template_name = 'members/dashboard.html'

    def get(self, request, *args, **kwargs):



        logged_member = None
        profile_photo_url = None

        tokens = UserSocialAuth.get_social_auth_for_user(request.user).get().tokens
        ig_session = InstagramSession(p_is_admin=False, p_token=tokens['access_token'])

        try:
            logged_member = Member.objects.get(django_user__username=request.user)

            profile_photo_url = None
            if logged_member.instagram_profile_picture_URL:
                profile_photo_url = logged_member.instagram_profile_picture_URL

        except ObjectDoesNotExist:
            logged_member = None

        # Limit calculation --------------------------------------------------------------
        x_ratelimit_remaining, x_ratelimit  = logged_member.get_api_limits()

        x_ratelimit_used = x_ratelimit - x_ratelimit_remaining
        if x_ratelimit != 0:
            x_limit_pct = (x_ratelimit_used / x_ratelimit) * 100
        else:
            x_limit_pct = 100
        # Limit calculation --------------------------------------------------------------

        return render(request,
                      self.template_name,
                      dict(logged_member=logged_member,
                           profile_photo_url=profile_photo_url,
                           x_ratelimit_remaining=x_ratelimit_remaining,
                           x_ratelimit=x_ratelimit,
                           x_limit_pct=x_limit_pct
                           )
        )


class MemberDisabledView(TemplateView):
    template_name = 'members/disabled.html'

    def get(self, request, *args, **kwargs):
        return render(request,
                      self.template_name,
                      dict(
                      )
        )


class MemberLogoutView(TemplateView):
    template_name = 'members/logout.html'

    def get(self, request, *args, **kwargs):
        auth_logout(request)

        return HttpResponseRedirect(reverse('lander:index'))