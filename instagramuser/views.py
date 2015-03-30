from __future__ import division
import decimal
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.utils import translation
from django.utils.datetime_safe import datetime
from django.utils.translation import ugettext as _
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from attributes.models import Attribute
from categories.models import Category
from instagramuser.models import InspiringUser
from libs.instagram.tools import InstagramSession, BestPhotos

from squaresensor.settings.base import IS_APP_LIVE
from .forms import AddInspiringUserForm
from members.models import Member
from photos.models import Photo

class AddInspiringUserView(TemplateView):
    """
    Add new Inspiring user
    """
    template_name = 'instagramuser/add.html'

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
        l_categories = Category.objects.all()
        l_attributes = Attribute.objects.all()
        # Common for all members views ===================================================
        try:
            logged_member = Member.objects.get(django_user__username=request.user)
            show_describe_button = logged_member.is_editor(request)
        except ObjectDoesNotExist:
            logged_member = None
        except:
            raise HttpResponseNotFound

        # Limit calculation --------------------------------------------------------------
        x_ratelimit_remaining, x_ratelimit = logged_member.get_api_limits()

        x_ratelimit_used = x_ratelimit - x_ratelimit_remaining
        if x_ratelimit != 0:
            x_limit_pct = (x_ratelimit_used / x_ratelimit) * 100
        else:
            x_limit_pct = 100
        # END Limit calculation ----------------------------------------------------------
        # END Common for all members views ===============================================

        form = AddInspiringUserForm()

        return render(request,
                      self.template_name,
                      dict(
                          form=form,

                          logged_member=logged_member,
                          x_ratelimit_remaining=x_ratelimit_remaining,
                          x_ratelimit=x_ratelimit,
                          x_limit_pct=x_limit_pct,
                          categories=l_categories,
                          attributes=l_attributes,
                          show_describe_button=show_describe_button,
                      )
        )


class AddInspiringUserByNameView(TemplateView):
    """
    Add inspiring user by name
    """


class InspiringUserIndexView(TemplateView):
    """
    List all inspiring users
    """

    template_name = 'instagramuser/index-inspiring-artists.html'

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

        # Limit calculation --------------------------------------------------------------
        x_ratelimit_remaining, x_ratelimit = logged_member.get_api_limits()

        x_ratelimit_used = x_ratelimit - x_ratelimit_remaining
        if x_ratelimit != 0:
            x_limit_pct = (x_ratelimit_used / x_ratelimit) * 100
        else:
            x_limit_pct = 100
        # END Limit calculation ----------------------------------------------------------
        # END Common for all members views ===============================================
        l_inspiring_users_queryset = InspiringUser.objects.all()

        return render(request,
                      self.template_name,
                      dict(
                          inspiring_users=l_inspiring_users_queryset,

                          logged_member=logged_member,
                          x_ratelimit_remaining=x_ratelimit_remaining,
                          x_ratelimit=x_ratelimit,
                          x_limit_pct=x_limit_pct,
                          categories=l_categories,
                          attributes=l_attributes,
                          )
        )



class InspiringUserNameView(TemplateView):
    template_name = 'instagramuser/recent-inspiring-artists.html'

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
        inspiring_user_id = kwargs['p_inspiring_user_id']

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

        # Limit calculation --------------------------------------------------------------
        x_ratelimit_remaining, x_ratelimit = logged_member.get_api_limits()

        x_ratelimit_used = x_ratelimit - x_ratelimit_remaining
        if x_ratelimit != 0:
            x_limit_pct = (x_ratelimit_used / x_ratelimit) * 100
        else:
            x_limit_pct = 100
        # END Limit calculation ----------------------------------------------------------
        # END Common for all members views ===============================================
        try:
            inspiring_user = InspiringUser.objects.get(id=inspiring_user_id)
        except ObjectDoesNotExist:
            inspiring_user = None
        except:
            raise
        if inspiring_user:
            l_token = logged_member.get_member_token(request)
            instagram_session = InstagramSession(p_is_admin=False, p_token=l_token['access_token'])
            instagram_session.init_instagram_API()
            user_search = instagram_session.is_instagram_user_valid(inspiring_user.instagram_user_name)

            if len(user_search) > 0:
                l_best_photos = BestPhotos(
                    instgram_user_id=inspiring_user.instagram_user_id,
                    top_n_photos=0,
                    search_photos_amount=50,
                    instagram_api=instagram_session
                )
                l_best_photos.get_instagram_photos()
                l_recent_media = l_best_photos.l_latest_photos

                l_good_photos = []
                for x_media in l_recent_media:
                    # filter out only the best
                    l_time_delta = datetime.today() - x_media.created_time
                    l_days = l_time_delta.days
                    l_like_count = x_media.like_count

                    #normalize
                    if (inspiring_user.poly_max_likes - inspiring_user.poly_min_likes) != 0:
                        l_like_count = (l_like_count - inspiring_user.poly_min_likes) / \
                                       (inspiring_user.poly_max_likes - inspiring_user.poly_min_likes)
                    else:
                        l_like_count = 0

                    if (inspiring_user.poly_max_days - inspiring_user.poly_min_days) != 0:
                        l_days = (l_days - inspiring_user.poly_min_days) / \
                                 (inspiring_user.poly_max_days - inspiring_user.poly_min_days)
                    else:
                        l_days = 0
                    #l_hour = l_time_delta.hour
                    l_prediction = inspiring_user.poly_theta_0 + inspiring_user.poly_theta_1*l_days + \
                                   inspiring_user.poly_theta_1*l_days*l_days

                    if l_prediction < l_like_count:
                        l_good_photos.extend([x_media])

        return render(request,
                      self.template_name,
                      dict(
                          photos=l_good_photos,
                          photos_owner=inspiring_user,

                          show_describe_button=False,
                          logged_member=logged_member,
                          x_ratelimit_remaining=x_ratelimit_remaining,
                          x_ratelimit=x_ratelimit,
                          x_limit_pct=x_limit_pct,
                          categories=l_categories,
                          attributes=l_attributes,
                          )
        )

