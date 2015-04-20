from __future__ import division
import logging
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.utils.datetime_safe import datetime
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout as auth_logout

# Create your views here.
from dateutil.relativedelta import relativedelta
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

from social_auth.db.django_models import UserSocialAuth
from attributes.models import Attribute
from categories.models import Category
from instagramuser.models import Follower, NewFriendContactedByMember
from libs.instagram.tools import InstagramSession, InstagramUserAdminUtils, update_member_limits_f, BestFollowers, \
    BestPhotos, InstagramComments
from .forms import MembershipForm

from .models import Member, Membership, Invoice
from squaresensor.settings.base import IMPORT_MAX_INSTAGRAM_FOLLOWERS, COMMENTER_NO_OF_PICS_MEMBER_LIMIT, \
    COMMENTER_NO_OF_PICS_NON_MEMBER_LIMIT, IS_PAYMENT_LIVE, PAYPAL_RECEIVER_EMAIL, ROOT_SITE_URL


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
            l_likes_in_last_minute, l_comments_in_last_minute = update_member_limits_f(request, logged_member)
            show_describe_button = logged_member.is_editor(request)
            # instagram_user = Member.objects.get(django_user__username=request.user)
            is_monthly_member = logged_member.is_monthly_member()
            is_yearly_member = logged_member.is_yearly_member()
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



        except ObjectDoesNotExist:
            logged_member = None

        l_categories = Category.objects.all()
        l_attributes = Attribute.objects.all()
        # Limit calculation --------------------------------------------------------------
        logged_member.refresh_api_limits(request)
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

                           is_monthly_member=is_monthly_member,
                           is_yearly_member=is_yearly_member,
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
            is_monthly_member = logged_member.is_monthly_member()
            is_yearly_member = logged_member.is_yearly_member()
            active_membership = logged_member.get_active_membership()

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
        # l_logged_members_categories = logged_member.categories
        #l_logged_members_attributes = logged_member.attributes



        return render(request,
                      self.template_name,
                      dict(
                          #logged_members_categories=l_logged_members_categories,
                          #logged_members_attributes=l_logged_members_categories,

                          is_monthly_member=is_monthly_member,
                          is_yearly_member=is_yearly_member,
                          active_membership=active_membership,
                          logged_member=logged_member,
                          x_ratelimit_remaining=x_ratelimit_remaining,
                          x_ratelimit=x_ratelimit,
                          x_limit_pct=x_limit_pct,
                          categories=l_categories,
                          attributes=l_attributes,
                      )
        )


def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # Undertake some action depending upon `ipn_obj`.

        try:
            paid_invoice = Invoice.objects.get(invoice_number=ipn_obj.invoice)
            paid_invoice.invoice_status = "paid"
            paid_invoice.save()
        except ObjectDoesNotExist:
            paid_invoice = None
        except:
            raise

        if paid_invoice:
            new_membership = Membership(membership_type=paid_invoice.membership_type,
                                        invoice=paid_invoice,
                                        member=paid_invoice.member)
            new_membership.save()
            logging.debug('Paid invoice %s' % (ipn_obj.invoice))
    else:
        try:
            paid_invoice = Invoice.objects.get(invoice_number=ipn_obj.invoice)
            paid_invoice.delete()
        except ObjectDoesNotExist:
            paid_invoice = None
        except:
            raise
        # something went wrong


class MemberNewMembershipView(TemplateView):
    template_name = 'members/new-membership.html'

    def get(self, request, *args, **kwargs):

        # Common for all members views ===================================================
        l_categories = Category.objects.all()
        l_attributes = Attribute.objects.all()
        try:
            logged_member = Member.objects.get(django_user__username=request.user)
            show_describe_button = logged_member.is_editor(request)
            is_monthly_member = logged_member.is_monthly_member()
            is_yearly_member = logged_member.is_yearly_member()
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

        return render(request,
                      self.template_name,
                      dict(
                           is_payment_live=IS_PAYMENT_LIVE,

                           is_monthly_member=is_monthly_member,
                           is_yearly_member=is_yearly_member,
                           logged_member=logged_member,
                           x_ratelimit_remaining=x_ratelimit_remaining,
                           x_ratelimit=x_ratelimit,
                           x_limit_pct=x_limit_pct,
                           categories=l_categories,
                           attributes=l_attributes,
                      )
        )


class MemberNewYearlyMembershipView(TemplateView):
    template_name = 'members/new-yearly-membership.html'

    def get(self, request, *args, **kwargs):

        # Common for all members views ===================================================
        l_categories = Category.objects.all()
        l_attributes = Attribute.objects.all()
        try:
            logged_member = Member.objects.get(django_user__username=request.user)
            show_describe_button = logged_member.is_editor(request)
            is_monthly_member = logged_member.is_monthly_member()
            is_yearly_member = logged_member.is_yearly_member()
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

        # Create a new invoice
        l_invoice_number = 'squaresensor-invoice-%s-%s' % (logged_member.instagram_user_name, str(datetime.now()))
        new_invoice = Invoice(member=logged_member,
                              invoice_number=l_invoice_number,
                              membership_type='PRO',
                              invoice_status='unpaid'
                              )
        new_invoice.save()

        paypal_dict = {
            "business": PAYPAL_RECEIVER_EMAIL,
            "amount": "50.00",
            "item_name": "Squaresensor Premium Yearly Membership",
            "invoice": l_invoice_number,
            "no-note": 1,
            "notify_url": ROOT_SITE_URL + reverse('paypal-ipn'),
            "return_url": ROOT_SITE_URL + reverse('members:new_membership_result'),
            "cancel_return": ROOT_SITE_URL + reverse('members:new_membership_cancel'),
        }

        form = PayPalPaymentsForm(initial=paypal_dict)
        valid_ipn_received.connect(show_me_the_money)

        return render(request,
                      self.template_name,
                      dict(form=form,
                           is_payment_live=IS_PAYMENT_LIVE,

                           is_monthly_member=is_monthly_member,
                           is_yearly_member=is_yearly_member,
                           logged_member=logged_member,
                           x_ratelimit_remaining=x_ratelimit_remaining,
                           x_ratelimit=x_ratelimit,
                           x_limit_pct=x_limit_pct,
                           categories=l_categories,
                           attributes=l_attributes,
                      )
        )



class MemberNewMonthlyMembershipView(TemplateView):
    template_name = 'members/new-monthly-membership.html'

    def get(self, request, *args, **kwargs):

        # Common for all members views ===================================================
        l_categories = Category.objects.all()
        l_attributes = Attribute.objects.all()
        try:
            logged_member = Member.objects.get(django_user__username=request.user)
            show_describe_button = logged_member.is_editor(request)
            is_monthly_member = logged_member.is_monthly_member()
            is_yearly_member = logged_member.is_yearly_member()
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

        # Create a new invoice
        l_invoice_number = 'squaresensor-invoice-%s-%s' % (logged_member.instagram_user_name, str(datetime.now()))
        new_invoice = Invoice(member=logged_member,
                              invoice_number=l_invoice_number,
                              membership_type='MON',
                              invoice_status='unpaid'
                              )
        new_invoice.save()

        paypal_dict = {
            "business": PAYPAL_RECEIVER_EMAIL,
            "amount": "5.00",
            "item_name": "Squaresensor Monthly Membership",
            "invoice": l_invoice_number,
            "no-note": 1,
            "notify_url": ROOT_SITE_URL + reverse('paypal-ipn'),
            "return_url": ROOT_SITE_URL + reverse('members:new_membership_result'),
            "cancel_return": ROOT_SITE_URL + reverse('members:new_membership_cancel'),
        }

        form = PayPalPaymentsForm(initial=paypal_dict)
        valid_ipn_received.connect(show_me_the_money)

        return render(request,
                      self.template_name,
                      dict(form=form,
                           is_payment_live=IS_PAYMENT_LIVE,

                           is_monthly_member=is_monthly_member,
                           is_yearly_member=is_yearly_member,
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

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        # do something
        return super(MemberNewMembershipResultView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):

        l_membership_end_time = None
        # Common for all members views ===================================================
        l_categories = Category.objects.all()
        l_attributes = Attribute.objects.all()
        try:
            logged_member = Member.objects.get(django_user__username=request.user)
            show_describe_button = logged_member.is_editor(request)
            is_monthly_member = logged_member.is_monthly_member()
            is_yearly_member = logged_member.is_yearly_member()
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

        """
        membership_form = MembershipForm(self.request.POST)

        if membership_form.is_valid():
            membership_type = membership_form.cleaned_data['membership_type']
            try:
                recurring_membership = membership_form.cleaned_data['recurring_membership']
            except:
                recurring_membership = u'off'
            membership_duration = membership_form.cleaned_data['membership_duration']
            l_membership_start_time = datetime.today()

            if membership_duration == 'MON':
                l_membership_end_time = l_membership_start_time + relativedelta(months=+1)
            if membership_duration == 'YEA':
                l_membership_end_time = l_membership_start_time + relativedelta(years=+1)
            if recurring_membership:
                l_recurring_membership = True
            else:
                l_recurring_membership = False

            # old_membership = logged_member.membership

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
        """

        return render(request,
                      self.template_name,
                      dict(

                          is_monthly_member=is_monthly_member,
                          is_yearly_member=is_yearly_member,
                          logged_member=logged_member,
                          x_ratelimit_remaining=x_ratelimit_remaining,
                          x_ratelimit=x_ratelimit,
                          x_limit_pct=x_limit_pct,
                          categories=l_categories,
                          attributes=l_attributes,
                      )
        )


class MemberNewMembershipCancelView(TemplateView):
    template_name = 'members/membership-cancel.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        # do something
        return super(MemberNewMembershipCancelView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):

        l_membership_end_time = None
        # Common for all members views ===================================================
        l_categories = Category.objects.all()
        l_attributes = Attribute.objects.all()
        try:
            logged_member = Member.objects.get(django_user__username=request.user)
            show_describe_button = logged_member.is_editor(request)
            is_monthly_member = logged_member.is_monthly_member()
            is_yearly_member = logged_member.is_yearly_member()
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
            l_membership_start_time = datetime.today()

            if membership_duration == 'MON':
                l_membership_end_time = l_membership_start_time + relativedelta(months=+1)
            if membership_duration == 'YEA':
                l_membership_end_time = l_membership_start_time + relativedelta(years=+1)
            if recurring_membership:
                l_recurring_membership = True
            else:
                l_recurring_membership = False

            # old_membership = logged_member.membership


        return render(request,
                      self.template_name,
                      dict(

                          is_monthly_member=is_monthly_member,
                          is_yearly_member=is_yearly_member,
                          logged_member=logged_member,
                          x_ratelimit_remaining=x_ratelimit_remaining,
                          x_ratelimit=x_ratelimit,
                          x_limit_pct=x_limit_pct,
                          categories=l_categories,
                          attributes=l_attributes,
                      )
        )


class MemberNewFriendsResponseView(TemplateView):
    template_name = 'members/new-friends-response.html'

    def get(self, request, *args, **kwargs):

        # Common for all members views ===================================================
        l_categories = Category.objects.all()
        l_attributes = Attribute.objects.all()
        try:
            logged_member = Member.objects.get(django_user__username=request.user)
            show_describe_button = logged_member.is_editor(request)
            is_monthly_member = logged_member.is_monthly_member()
            is_yearly_member = logged_member.is_yearly_member()
        except ObjectDoesNotExist:
            logged_member = None
        except:
            raise HttpResponseNotFound
        # END Common for all members views ===============================================

        l_token = logged_member.get_member_token(request)
        instagram_session = InstagramSession(p_is_admin=False, p_token=l_token['access_token'])
        instagram_session.init_instagram_API()

        l_members_followers_obj = BestFollowers(
            p_instgram_user_id=logged_member.instagram_user_id,
            p_analyze_n_photos=IMPORT_MAX_INSTAGRAM_FOLLOWERS,
            p_instagram_api=instagram_session
        )
        l_members_followers = l_members_followers_obj.get_all_instagram_followers(request, logged_member)

        l_contacted_new_friends = NewFriendContactedByMember.objects.filter(
            member=logged_member,
        ).exclude(interaction_type='S')

        l_new_friends_since_last_check = 0
        l_total_new_squaresensor_friends = 0
        l_contacted_new_friends_cnt = 0
        l_new_friends_list = []
        l_existing_friends_list = []
        if l_contacted_new_friends.count() > 0:
            l_found = False
            for contacted_friend in l_contacted_new_friends:
                l_contacted_new_friends_cnt += 1
                for follower in l_members_followers:
                    if follower.username == contacted_friend.friend.instagram_user_name:
                        l_found = True
                        l_total_new_squaresensor_friends += 1
                        if contacted_friend.response_date == None:
                            l_new_friends_list.extend([follower])
                            l_new_friends_since_last_check += 1
                        else:
                            l_existing_friends_list.extend([follower])

        # Limit calculation --------------------------------------------------------------
        logged_member.refresh_api_limits(request)
        x_ratelimit_remaining, x_ratelimit = logged_member.get_api_limits()

        x_ratelimit_used = x_ratelimit - x_ratelimit_remaining
        if x_ratelimit != 0:
            x_limit_pct = (x_ratelimit_used / x_ratelimit) * 100
        else:
            x_limit_pct = 100
        # END Limit calculation ----------------------------------------------------------

        return render(request,
                      self.template_name,
                      dict(
                          new_friends_list=l_new_friends_list,
                          existing_friends_list=l_existing_friends_list,
                          contacted_new_friends_cnt=l_contacted_new_friends_cnt,
                          new_friends_since_last_check=l_new_friends_since_last_check,
                          total_new_squaresensor_friends=l_total_new_squaresensor_friends,

                          is_monthly_member=is_monthly_member,
                          is_yearly_member=is_yearly_member,
                          logged_member=logged_member,
                          x_ratelimit_remaining=x_ratelimit_remaining,
                          x_ratelimit=x_ratelimit,
                          x_limit_pct=x_limit_pct,
                          categories=l_categories,
                          attributes=l_attributes,
                      )
        )


class CommenterIndexView(TemplateView):
    template_name = 'members/commenter-index.html'

    def get(self, request, *args, **kwargs):

        # Common for all members views ===================================================
        l_categories = Category.objects.all()
        l_attributes = Attribute.objects.all()
        is_monthly_member = None
        is_yearly_member = None
        try:
            logged_member = Member.objects.get(django_user__username=request.user)
            show_describe_button = logged_member.is_editor(request)
            is_monthly_member = logged_member.is_monthly_member()
            is_yearly_member = logged_member.is_yearly_member()
        except ObjectDoesNotExist:
            logged_member = None
        except:
            raise HttpResponseNotFound
        # END Common for all members views ===============================================

        l_token = logged_member.get_member_token(request)
        instagram_session = InstagramSession(p_is_admin=False, p_token=l_token['access_token'])
        instagram_session.init_instagram_API()

        if logged_member.is_monthly_member() or logged_member.is_yearly_member():
            l_search_photos_amount = COMMENTER_NO_OF_PICS_MEMBER_LIMIT
        else:
            l_search_photos_amount = COMMENTER_NO_OF_PICS_NON_MEMBER_LIMIT

        l_member_photos_obj = BestPhotos(
            instgram_user_id=logged_member.instagram_user_id,
            top_n_photos=None,
            search_photos_amount=l_search_photos_amount,
            instagram_api=instagram_session
        )
        l_member_photos_obj.get_instagram_photos()
        l_member_latest_photos = l_member_photos_obj.l_latest_photos

        l_unanswered_comments_and_posts_list = []
        for photo in l_member_latest_photos:
            if photo.comment_count > 0:
                l_instagram_comments = InstagramComments(
                    p_photo_id=photo.id,
                    p_instagram_session=instagram_session
                )

                l_unanswered_comments_list = l_instagram_comments.get_unanswered_comments(
                    logged_member.instagram_user_id
                )

                l_unanswered_comments_list_length = len(l_unanswered_comments_list)

                if l_unanswered_comments_list_length > 0:
                    l_unanswered_comments_and_posts_list.append(
                        [photo.get_thumbnail_url(),
                         l_unanswered_comments_list,
                         len(l_unanswered_comments_list),
                         photo.id
                        ]
                    )


        # Limit calculation --------------------------------------------------------------
        logged_member.refresh_api_limits(request)
        x_ratelimit_remaining, x_ratelimit = logged_member.get_api_limits()

        x_ratelimit_used = x_ratelimit - x_ratelimit_remaining
        if x_ratelimit != 0:
            x_limit_pct = (x_ratelimit_used / x_ratelimit) * 100
        else:
            x_limit_pct = 100
        # END Limit calculation ----------------------------------------------------------

        return render(request,
                      self.template_name,
                      dict(
                          unanswered_comments_media_list=l_unanswered_comments_and_posts_list,
                          search_photos_amount=l_search_photos_amount,

                          is_monthly_member=is_monthly_member,
                          is_yearly_member=is_yearly_member,
                          membership_allowance=COMMENTER_NO_OF_PICS_MEMBER_LIMIT,
                          logged_member=logged_member,
                          x_ratelimit_remaining=x_ratelimit_remaining,
                          x_ratelimit=x_ratelimit,
                          x_limit_pct=x_limit_pct,
                          categories=l_categories,
                          attributes=l_attributes,
                      )
        )