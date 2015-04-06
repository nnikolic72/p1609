from __future__ import division
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.utils import translation
from django.utils.datetime_safe import datetime
from django.utils.translation import ugettext as _
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from libs.instagram.tools import SmartFeedHelper, InstagramSession, MyLikes

from squaresensor.settings.base import (
    SMART_FEED_BATCH_SIZE, SMART_FEED_MAX_LOAD_PICS,
    MIN_SQUAREFOLLOWINGS)

from attributes.models import Attribute
from categories.models import Category
from members.models import Member
from .models import SquareFollowing


class SmartFeedIndexView(TemplateView):
    """
    Index view, displays list of categories
    """

    template_name = 'smartfeed/index.html'

    def get(self, request, *args, **kwargs):
        """
        Handle get request - display photos and all controls

        :param request:
        :type request:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """

        liked_photos = None
        l_squarefollowings_count = None
        l_best_media = None

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

        l_squarefollowings_count = SquareFollowing.objects.filter(member_id2=logged_member).count()
        if l_squarefollowings_count >= MIN_SQUAREFOLLOWINGS:

            # END Common for all members views ===============================================
            l_squarefollowing_queryset = SquareFollowing.objects.all()

            l_token = logged_member.get_member_token(request)
            instagram_session = InstagramSession(p_is_admin=False, p_token=l_token['access_token'])
            instagram_session.init_instagram_API()

            l_smart_feed_helper = SmartFeedHelper(
                p_feed_owner_instagram_id=logged_member.instagram_user_id,
                p_instagram_session=instagram_session,
                p_batch_size=SMART_FEED_BATCH_SIZE,
                p_min_id=logged_member.smartfeed_last_seen_instagram_photo_id
            )
            l_best_media = l_smart_feed_helper.find_best_media(
                p_media_to_return=SMART_FEED_BATCH_SIZE,
                p_starting_media_id=None,
                p_logged_member=logged_member,
                p_max_days=30
            )

            liked_photos = []
            for x_media in l_best_media:
                my_likes = MyLikes(request.user.username, x_media.id, instagram_session )
                has_user_liked_media, no_of_likes = my_likes.has_user_liked_media()
                if has_user_liked_media:
                    liked_photos.extend([x_media.id])


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
                          best_media=l_best_media,
                          liked_photos=liked_photos,
                          squarefollowings_count=l_squarefollowings_count,
                          new_friends_interaction=0,

                          logged_member=logged_member,
                          x_ratelimit_remaining=x_ratelimit_remaining,
                          x_ratelimit=x_ratelimit,
                          x_limit_pct=x_limit_pct,
                          categories=l_categories,
                          attributes=l_attributes,
                          )
        )


class SmartFeedConfigureCalendarView(TemplateView):
    """

    """
    """
    Index view, displays list of categories
    """

    template_name = 'smartfeed/index.html'

    def get(self, request, *args, **kwargs):
        """
        Handle get request - display photos and all controls

        :param request:
        :type request:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        p_period_str = kwargs['p_period']
        l_best_media = None
        liked_photos = None
        p_period_verbose = None

        try:
            p_period = int(p_period_str)
        except:
            raise

        if p_period == 0:
            p_period_verbose = _('today')
        if p_period == 1:
            p_period_verbose = _('1 day ago')
        if p_period == 2:
            p_period_verbose = str(p_period) + _(' days ago')


        date_from = datetime.today() - timedelta(days=p_period+1)
        date_from_to = datetime.today() - timedelta(days=p_period)

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
        l_squarefollowing_queryset = SquareFollowing.objects.all()
        l_squarefollowings_count = SquareFollowing.objects.filter(member_id2=logged_member).count()
        if l_squarefollowings_count >= MIN_SQUAREFOLLOWINGS:

            l_token = logged_member.get_member_token(request)
            instagram_session = InstagramSession(p_is_admin=False, p_token=l_token['access_token'])
            instagram_session.init_instagram_API()
            l_squarefollowings_count = SquareFollowing.objects.filter(member_id2=logged_member).count()
            if l_squarefollowings_count >= MIN_SQUAREFOLLOWINGS:
                l_smart_feed_helper = SmartFeedHelper(
                    p_feed_owner_instagram_id=logged_member.instagram_user_id,
                    p_instagram_session=instagram_session,
                    p_batch_size=SMART_FEED_BATCH_SIZE,
                    p_min_id=None,
                    p_date_from=date_from,
                    p_date_to=date_from_to
                )
                l_best_media = l_smart_feed_helper.find_best_media(
                    p_media_to_return=SMART_FEED_BATCH_SIZE,
                    p_starting_media_id=None,
                    p_logged_member=logged_member,
                    p_max_days=30
                )



                liked_photos = []
                for x_media in l_best_media:
                    my_likes = MyLikes(request.user.username, x_media.id, instagram_session )
                    has_user_liked_media, no_of_likes = my_likes.has_user_liked_media()
                    if has_user_liked_media:
                        liked_photos.extend([x_media.id])


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
                          best_media=l_best_media,
                          liked_photos=liked_photos,
                          period_verbose=p_period_verbose,
                          period_number=p_period,
                          squarefollowings_count=l_squarefollowings_count,
                          new_friends_interaction=0,

                          logged_member=logged_member,
                          x_ratelimit_remaining=x_ratelimit_remaining,
                          x_ratelimit=x_ratelimit,
                          x_limit_pct=x_limit_pct,
                          categories=l_categories,
                          attributes=l_attributes,
                          )
        )


class SmartFeedConfigureView(TemplateView):
    """
    Index view, displays list of categories
    """

    template_name = 'smartfeed/configure.html'

    def get(self, request, *args, **kwargs):
        """
        Handle get request - display photos and all controls

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
        l_squarefollowing_queryset = SquareFollowing.objects.filter(member_id2=logged_member)

        #for x in l_squarefollowing_queryset:
        #    for y in x.

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
                          l_squarefollowing_queryset=l_squarefollowing_queryset,

                          logged_member=logged_member,
                          x_ratelimit_remaining=x_ratelimit_remaining,
                          x_ratelimit=x_ratelimit,
                          x_limit_pct=x_limit_pct,
                          categories=l_categories,
                          attributes=l_attributes,
                          )
        )
