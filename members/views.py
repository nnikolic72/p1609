from __future__ import division
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.utils.datetime_safe import datetime
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout as auth_logout

# Create your views here.
from dateutil.relativedelta import relativedelta
from django.views.generic import TemplateView
from social_auth.db.django_models import UserSocialAuth
from attributes.models import Attribute
from categories.models import Category
from libs.instagram.tools import InstagramSession, InstagramUserAdminUtils
from .forms import MembershipForm


from .models import Member, Membership


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
            show_describe_button = logged_member.is_editor(request)
            #instagram_user = Member.objects.get(django_user__username=request.user)
            queryset = Member.objects.filter(django_user__username=request.user)

            for q in queryset:
                q.to_be_processed_for_basic_info = True
                #q.to_be_processed_for_photos = True
                q.save()

            l_token = logged_member.get_member_token(request)
            instagram_session = InstagramSession(p_is_admin=False, p_token=l_token['access_token'])
            instagram_session.init_instagram_API()
            user_search = instagram_session.is_instagram_user_valid(request.user)

            ig_utils = InstagramUserAdminUtils()
            ig_utils.process_instagram_user(request, queryset)
            logged_member = Member.objects.get(django_user__username=request.user)

            profile_photo_url = None
            if logged_member.instagram_profile_picture_URL:
                profile_photo_url = logged_member.instagram_profile_picture_URL

            l_categories = Category.objects.all()
            l_attributes = Attribute.objects.all()

        except ObjectDoesNotExist:
            logged_member = None


        # Limit calculation --------------------------------------------------------------
        x_ratelimit_remaining, x_ratelimit = logged_member.get_api_limits()

        x_ratelimit_used = x_ratelimit - x_ratelimit_remaining
        if x_ratelimit != 0:
            x_limit_pct = (x_ratelimit_used / x_ratelimit) * 100
        else:
            x_limit_pct = 100
        # Limit calculation --------------------------------------------------------------

        return render(request,
                      self.template_name,
                      dict(photo_owner=logged_member,
                           logged_member=logged_member,
                           profile_photo_url=profile_photo_url,
                           x_ratelimit_remaining=x_ratelimit_remaining,
                           x_ratelimit=x_ratelimit,
                           x_limit_pct=x_limit_pct,
                           categories=l_categories,
                           attributes=l_attributes,
                           show_describe_button=show_describe_button,
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


class MemberMyAccountView(TemplateView):
    template_name = 'members/my_account.html'

    def get(self, request, *args, **kwargs):
        """

        :param request:
        :type request:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """

        # Common for all members views ===================================================
        l_categories = Category.objects.all()
        l_attributes = Attribute.objects.all()
        try:
            logged_member = Member.objects.get(django_user__username=request.user)
            show_describe_button = logged_member.is_editor(request)
        except ObjectDoesNotExist:
            logged_member = None
        except:
            raise HttpResponseNotFound


        # END Common for all members views ===============================================

        # Limit calculation --------------------------------------------------------------
        logged_member.refresh_api_limits(request)
        x_ratelimit_remaining, x_ratelimit = logged_member.get_api_limits()

        x_ratelimit_used = x_ratelimit - x_ratelimit_remaining
        if x_ratelimit != 0:
            x_limit_pct = (x_ratelimit_used / x_ratelimit) * 100
        else:
            x_limit_pct = 100
        # END Limit calculation ----------------------------------------------------------
        #l_logged_members_categories = logged_member.categories
        #l_logged_members_attributes = logged_member.attributes



        return render(request,
                      self.template_name,
                      dict(
                          #logged_members_categories=l_logged_members_categories,
                        #logged_members_attributes=l_logged_members_categories,

                          logged_member=logged_member,
                          x_ratelimit_remaining=x_ratelimit_remaining,
                          x_ratelimit=x_ratelimit,
                          x_limit_pct=x_limit_pct,
                          categories=l_categories,
                          attributes=l_attributes,
                          )
        )


class MemberNewMembershipView(TemplateView):

    template_name = 'members/new-membership.html'

    def get(self, request, *args, **kwargs):

        # Common for all members views ===================================================
        l_categories = Category.objects.all()
        l_attributes = Attribute.objects.all()
        try:
            logged_member = Member.objects.get(django_user__username=request.user)
            show_describe_button = logged_member.is_editor(request)
        except ObjectDoesNotExist:
            logged_member = None
        except:
            raise HttpResponseNotFound


        # END Common for all members views ===============================================

        # Limit calculation --------------------------------------------------------------
        logged_member.refresh_api_limits(request)
        x_ratelimit_remaining, x_ratelimit = logged_member.get_api_limits()

        x_ratelimit_used = x_ratelimit - x_ratelimit_remaining
        if x_ratelimit != 0:
            x_limit_pct = (x_ratelimit_used / x_ratelimit) * 100
        else:
            x_limit_pct = 100
        # END Limit calculation ----------------------------------------------------------

        form = MembershipForm()

        return render(request,
                      self.template_name,
                      dict(form=form,

                          logged_member=logged_member,
                          x_ratelimit_remaining=x_ratelimit_remaining,
                          x_ratelimit=x_ratelimit,
                          x_limit_pct=x_limit_pct,
                          categories=l_categories,
                          attributes=l_attributes,
                          )
        )


class MemberNewMembershipResultView(TemplateView):

    template_name = 'members/membership-result.html'

    def post(self, request, *args, **kwargs):

        # Common for all members views ===================================================
        l_categories = Category.objects.all()
        l_attributes = Attribute.objects.all()
        try:
            logged_member = Member.objects.get(django_user__username=request.user)
            show_describe_button = logged_member.is_editor(request)
        except ObjectDoesNotExist:
            logged_member = None
        except:
            raise HttpResponseNotFound


        # END Common for all members views ===============================================

        # Limit calculation --------------------------------------------------------------
        logged_member.refresh_api_limits(request)
        x_ratelimit_remaining, x_ratelimit = logged_member.get_api_limits()

        x_ratelimit_used = x_ratelimit - x_ratelimit_remaining
        if x_ratelimit != 0:
            x_limit_pct = (x_ratelimit_used / x_ratelimit) * 100
        else:
            x_limit_pct = 100
        # END Limit calculation ----------------------------------------------------------

        membership_form = MembershipForm(self.request.POST)

        if membership_form.is_valid():
            membership_type = membership_form.cleaned_data['membership_type']
            try:
                recurring_membership = membership_form.cleaned_data['recurring_membership']
            except:
                recurring_membership = u'off'
            membership_duration = membership_form.cleaned_data['membership_duration']
            l_membership_start_time=datetime.today()

            if membership_duration == 'MON':
                l_membership_end_time = l_membership_start_time + relativedelta(months=+1)
            if membership_duration == 'YEA':
                l_membership_end_time = l_membership_start_time + relativedelta(years=+1)
            if recurring_membership == True:
                l_recurring_membership = True
            else:
                l_recurring_membership = False

            #old_membership = logged_member.membership


            l_new_membership = Membership(
                membership_type=membership_type,
                membership_start_time=l_membership_start_time,
                membership_end_time=l_membership_end_time,
                recurring_membership=l_recurring_membership,
                active_membership=True
            )
            try:
                l_new_membership.save()
                for membership in logged_member.membership.all():
                    membership.active_membership = False
                    membership.save()
                #old_membership.save()
                logged_member.membership.add(l_new_membership)
                #logged_member.membership.remove(old_membership)
                #logged_member.save()
            except:
                raise


        return render(request,
                      self.template_name,
                      dict(

                          logged_member=logged_member,
                          x_ratelimit_remaining=x_ratelimit_remaining,
                          x_ratelimit=x_ratelimit,
                          x_limit_pct=x_limit_pct,
                          categories=l_categories,
                          attributes=l_attributes,
                          )
        )