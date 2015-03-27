from __future__ import division
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.utils import translation
from django.utils.translation import ugettext as _
from django.views.generic import FormView
from django.views.generic.base import TemplateView

from libs.instagram.tools import InstagramSession, BestPhotos, InstagramUserAdminUtils

from .models import Photo

from squaresensor.settings.base import (
    INSPIRING_USERS_FIND_TOP_N_PHOTOS,
    INSPIRING_USERS_SEARCH_N_PHOTOS,
    FOLLOWINGS_FIND_TOP_N_PHOTOS,
    FOLLOWINGS_SEARCH_N_PHOTOS,
    FRIENDS_FIND_TOP_N_PHOTOS,
    FRIENDS_SEARCH_N_PHOTOS,
    MEMBERS_FIND_TOP_N_PHOTOS,
    MEMBERS_SEARCH_N_PHOTOS,
)

from instagramuser.models import Follower, Following, InspiringUser
from members.models import Member


# Create your views here.
class UsersBestPhotosView(TemplateView):
    """
    displays users best photos
    """
    template_name = 'photos/allbest.html'

    is_member = False
    is_follower = False
    is_following = False
    is_inspiring = False
    is_none = True
    instagram_user = None

    def find_squaresensor_user(self, p_username):
        """
        init the class
        :param p_username:
        :type p_username:
        :return:
        :rtype:
        """

        self.is_none = True

        try:
            self.instagram_user = Member.objects.get(django_user__username=p_username)
            self.queryset = Member.objects.filter(django_user__username=p_username)
            self.is_member = True

        except ObjectDoesNotExist:
            self.is_member = False
        except:
            raise HttpResponseNotFound

        if not self.is_member:
            try:
                self.instagram_user = InspiringUser.objects.get(instagram_user_name=p_username)
                self.queryset = InspiringUser.objects.filter(instagram_user_name=p_username)
                self.is_inspiring = True
            except ObjectDoesNotExist:
                self.is_inspiring = False
            except:
                raise HttpResponseNotFound

            if not self.is_inspiring:
                try:
                    self.instagram_user = Follower.objects.get(instagram_user_name=p_username)
                    self.queryset = Follower.objects.filter(instagram_user_name=p_username)
                    self.is_follower = True
                except ObjectDoesNotExist:
                    self.is_follower = False
                except:
                    raise HttpResponseNotFound

                if not self.is_follower:
                    try:
                        self.instagram_user = Following.objects.get(instagram_user_name=p_username)
                        self.queryset = Following.objects.filter(instagram_user_name=p_username)
                        self.is_following = True
                    except ObjectDoesNotExist:
                        self.is_following = False
                    except:
                        raise HttpResponseNotFound

        return self.instagram_user, self.queryset

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
        instagram_user_name = kwargs['p_username']
        mode = kwargs['p_mode']

        squaresensor_user, queryset = self.find_squaresensor_user(instagram_user_name)


        # Common for all members views ===================================================
        try:
            logged_member = Member.objects.get(django_user__username=request.user)
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

        if self.is_member:
            l_photos_queryset = Photo.objects.filter(member_id=squaresensor_user).order_by('-photo_rating')

        if self.is_inspiring:
            l_photos_queryset = Photo.objects.filter(inspiring_user_id=squaresensor_user).order_by('-photo_rating')

        if self.is_follower:
            l_photos_queryset = Photo.objects.filter(follower_id=squaresensor_user).order_by('-photo_rating')

        if self.is_following:
            l_photos_queryset = Photo.objects.filter(following_id=squaresensor_user).order_by('-photo_rating')

        if (not l_photos_queryset) or (mode == 'refresh'):
            l_token = logged_member.get_member_token(request)
            instagram_session = InstagramSession(p_is_admin=False, p_token=l_token['access_token'])
            instagram_session.init_instagram_API()
            user_search = instagram_session.is_instagram_user_valid(instagram_user_name)

            ig_utils = InstagramUserAdminUtils()
            ig_utils.process_instagram_user(request, queryset)

            if self.is_member:
                l_photos_queryset = Photo.objects.filter(member_id=squaresensor_user).order_by('-photo_rating')

            if self.is_inspiring:
                l_photos_queryset = Photo.objects.filter(inspiring_user_id=squaresensor_user).order_by('-photo_rating')

            if self.is_follower:
                l_photos_queryset = Photo.objects.filter(follower_id=squaresensor_user).order_by('-photo_rating')

            if self.is_following:
                l_photos_queryset = Photo.objects.filter(following_id=squaresensor_user).order_by('-photo_rating')

            if l_photos_queryset:
                ig_utils.process_photos_by_instagram_api(request, l_photos_queryset)

        # Limit calculation --------------------------------------------------------------
        x_ratelimit_remaining, x_ratelimit = logged_member.refresh_api_limits(request)

        x_ratelimit_used = x_ratelimit - x_ratelimit_remaining
        if x_ratelimit != 0:
            x_limit_pct = (x_ratelimit_used / x_ratelimit) * 100
        else:
            x_limit_pct = 100
        # END Limit calculation ----------------------------------------------------------

        return render(request,
                      self.template_name,
                      dict(
                          photos=l_photos_queryset,

                          logged_member=logged_member,
                          x_ratelimit_remaining=x_ratelimit_remaining,
                          x_ratelimit=x_ratelimit,
                          x_limit_pct=x_limit_pct
                          )
        )
