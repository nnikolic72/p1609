from __future__ import division
import decimal
from datetime import timedelta
from django.utils import timezone
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
from instagramuser.models import InspiringUser, Following, Follower, FollowerBelongsToCategory, \
    FollowerBelongsToAttribute, InspiringUserBelongsToCategory, InspiringUserBelongsToAttribute
from libs.instagram.tools import InstagramSession, BestPhotos, InstagramUserAdminUtils, MyLikes

from squaresensor.settings.base import IS_APP_LIVE, FRIENDS_FIND_TOP_N_PHOTOS, FRIENDS_SEARCH_N_PHOTOS, \
    FIND_NEW_FRIENDS_MAX_MEMBER_DAILY_INTERACTIONS, FIND_NEW_FRIENDS_MAX_NON_MEMBER_DAILY_INTERACTIONS, \
    FIND_FRIENDS_LIMIT_PERIOD_RESET_TIME_DAYS, RECENT_BEST_SEARCH_LAST_N_PHOTOS, TEST_APP
from .forms import AddInspiringUserForm
from members.models import Member, MemberBelongsToCategory, MemberBelongsToAttribute
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
            is_monthly_member = logged_member.is_monthly_member()
            is_yearly_member = logged_member.is_yearly_member()
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

                          is_monthly_member=is_monthly_member,
                          is_yearly_member=is_yearly_member,
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
    pass


class InspiringUserIndexView(TemplateView):
    """
    List all inspiring users
    """

    template_name = 'instagramuser/index-inspiring-artists2.html'

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
            is_monthly_member = logged_member.is_monthly_member()
            is_yearly_member = logged_member.is_yearly_member()
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
        inspiring_user_name = kwargs['p_inspiring_user_name']
        l_good_photos = None

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
            inspiring_user = InspiringUser.objects.get(instagram_user_name=inspiring_user_name)
        except ObjectDoesNotExist:
            inspiring_user = None
        except:
            raise
        if inspiring_user:
            l_token = logged_member.get_member_token(request)
            instagram_session = InstagramSession(p_is_admin=False, p_token=l_token['access_token'])
            instagram_session.init_instagram_API()
            user_search = instagram_session.is_instagram_user_valid(inspiring_user.instagram_user_name)

            if (len(user_search) > 0) and (user_search[0].username == inspiring_user.instagram_user_name ):
                l_instagram_user = instagram_session.get_instagram_user(user_search[0].id)
                l_best_photos = BestPhotos(
                    instgram_user_id=inspiring_user.instagram_user_id,
                    top_n_photos=0,
                    search_photos_amount=50,
                    instagram_api=instagram_session
                )
                l_best_photos.get_instagram_photos()
                l_recent_media = l_best_photos.l_latest_photos


                l_good_photos = []
                liked_photos = []
                for x_media in l_recent_media:
                    # filter out only the best
                    l_time_delta = datetime.today() - x_media.created_time
                    l_days = l_time_delta.days
                    l_like_count = x_media.like_count

                    my_likes = MyLikes(request.user.username, x_media.id, instagram_session )
                    has_user_liked_media, no_of_likes = my_likes.has_user_liked_media()
                    if has_user_liked_media:
                        liked_photos.extend([x_media.id])

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
                          photos_owner=inspiring_user.instagram_user_name,
                          liked_photos=liked_photos,
                          instagramuser=l_instagram_user,
                          new_friends_interaction=0,

                          is_monthly_member=is_monthly_member,
                          is_yearly_member=is_yearly_member,
                          show_describe_button=False,
                          logged_member=logged_member,
                          x_ratelimit_remaining=x_ratelimit_remaining,
                          x_ratelimit=x_ratelimit,
                          x_limit_pct=x_limit_pct,
                          categories=l_categories,
                          attributes=l_attributes,
                          )
        )


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


    def post(self, request, *args, **kwargs):
        x=1
        pass

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

        show_describe_button = False
        liked_photos = []


        squaresensor_user, queryset = self.find_squaresensor_user(instagram_user_name)


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

        for q in queryset:
            q.to_be_processed_for_basic_info = True
            q.to_be_processed_for_photos = True
            q.save()
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
        else:

            if self.is_inspiring:
                l_photos_queryset = Photo.objects.filter(inspiring_user_id=squaresensor_user).order_by('-photo_rating')
            else:

                if self.is_follower:
                    l_photos_queryset = Photo.objects.filter(follower_id=squaresensor_user).order_by('-photo_rating')
                else:

                    if self.is_following:
                        l_photos_queryset = Photo.objects.filter(following_id=squaresensor_user).order_by('-photo_rating')

        l_token = logged_member.get_member_token(request)
        instagram_session = InstagramSession(p_is_admin=False, p_token=l_token['access_token'])
        instagram_session.init_instagram_API()

        if (l_photos_queryset.count() == 0) or (mode == 'refresh'):
            for q in queryset:
                q.to_be_processed_for_basic_info = True
                q.to_be_processed_for_photos = True
                q.save()
            ig_admin_utils = InstagramUserAdminUtils(p_is_admin=False, p_token=l_token['access_token'])
            ig_admin_utils.process_instagram_user(queryset)

            user_search = instagram_session.is_instagram_user_valid(instagram_user_name)

            if self.is_member:
                l_photos_queryset = Photo.objects.filter(member_id=squaresensor_user).order_by('-photo_rating')
            else:
                if self.is_inspiring:
                    l_photos_queryset = Photo.objects.filter(inspiring_user_id=squaresensor_user).order_by('-photo_rating')
                else:

                    if self.is_follower:
                        l_photos_queryset = Photo.objects.filter(follower_id=squaresensor_user).order_by('-photo_rating')
                    else:

                        if self.is_following:
                            l_photos_queryset = Photo.objects.filter(following_id=squaresensor_user).order_by('-photo_rating')



            if self.is_member:
                l_photos_queryset = Photo.objects.filter(member_id=squaresensor_user).order_by('-photo_rating')
            else:

                if self.is_inspiring:
                    l_photos_queryset = Photo.objects.filter(inspiring_user_id=squaresensor_user).order_by('-photo_rating')
                else:

                    if self.is_follower:
                        l_photos_queryset = Photo.objects.filter(follower_id=squaresensor_user).order_by('-photo_rating')
                    else:

                        if self.is_following:
                            l_photos_queryset = Photo.objects.filter(following_id=squaresensor_user).order_by('-photo_rating')

        ig_utils = InstagramUserAdminUtils(p_is_admin=False, p_token=l_token['access_token'])
        ig_utils.process_instagram_user(queryset)
        if (l_photos_queryset.count() > 0):
            ig_utils.process_photos_by_instagram_api(l_photos_queryset)

        liked_photos = []
        for x_media in l_photos_queryset:
            my_likes = MyLikes(request.user.username, x_media.instagram_photo_id, instagram_session )
            has_user_liked_media, no_of_likes = my_likes.has_user_liked_media()
            if has_user_liked_media:
                liked_photos.extend([x_media.instagram_photo_id])

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
                          show_describe_button=show_describe_button,
                          photo_owner=squaresensor_user,
                          liked_photos=liked_photos,
                          new_friends_interaction=0,
                          og_url=request.build_absolute_uri(),

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


class AnyUserRecentBestView(TemplateView):
    """
    Calculates and Display andy user recent best
    """
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
        instagram_user_name = kwargs['p_instagram_user_name']

        l_good_photos = None
        liked_photos = None
        l_instagram_user = None

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
        user_search = instagram_session.is_instagram_user_valid(instagram_user_name)

        if (len(user_search) > 0) and (user_search[0].username == instagram_user_name):
            l_instagram_user = instagram_session.get_instagram_user(user_search[0].id)

            l_best_photos = BestPhotos(
                instgram_user_id=l_instagram_user.id,
                top_n_photos=0,
                search_photos_amount=RECENT_BEST_SEARCH_LAST_N_PHOTOS,
                instagram_api=instagram_session
            )
            l_best_photos.get_instagram_photos()
            l_recent_media = l_best_photos.l_latest_photos

            l_top_photos = None
            if l_best_photos.l_user_has_photos:
                l_polynom, l_max_days, l_min_days, l_max_likes, l_min_likes = l_best_photos.get_top_photos()

            l_good_photos = []
            liked_photos = []
            for x_media in l_recent_media:
                # filter out only the best
                l_time_delta = datetime.today() - x_media.created_time
                l_days = l_time_delta.days
                l_like_count = x_media.like_count

                my_likes = MyLikes(request.user.username, x_media.id, instagram_session )
                has_user_liked_media, no_of_likes = my_likes.has_user_liked_media()
                if has_user_liked_media:
                    liked_photos.extend([x_media.id])

                poly_theta_2 = l_polynom.coeffs[0]
                poly_theta_1 = l_polynom.coeffs[1]
                poly_theta_0 = l_polynom.coeffs[2]

                #normalize
                if (l_max_likes - l_min_likes) != 0:
                    l_like_count = (l_like_count - l_min_likes) / \
                                   (l_max_likes - l_min_likes)
                else:
                    l_like_count = 0

                if (l_max_days - l_min_days) != 0:
                    l_days = (l_days - l_min_days) / \
                             (l_max_days - l_min_days)
                else:
                    l_days = 0
                #l_hour = l_time_delta.hour
                l_prediction = poly_theta_0 + poly_theta_1*l_days + \
                               poly_theta_1*l_days*l_days

                if l_prediction < l_like_count:
                    l_good_photos.extend([x_media])


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
                          photos=l_good_photos,
                          photos_owner=instagram_user_name,
                          liked_photos=liked_photos,
                          instagramuser=l_instagram_user,
                          new_friends_interaction=0,

                          is_monthly_member=is_monthly_member,
                          is_yearly_member=is_yearly_member,
                          show_describe_button=False,
                          logged_member=logged_member,
                          x_ratelimit_remaining=x_ratelimit_remaining,
                          x_ratelimit=x_ratelimit,
                          x_limit_pct=x_limit_pct,
                          categories=l_categories,
                          attributes=l_attributes,
                          )
        )


class FindFriendsView(TemplateView):
    """
    Class to display a list of new friends candidates
    """
    template_name = 'instagramuser/find-new-friends.html'

    def get(self, request, *args, **kwargs):
        """
        Handle get request - display new friends, their photos and all controls

        :param request:
        :type request:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """

        liked_photos = []
        max_interactions = None
        l_new_friends_remaining = None
        show_describe_button = None
        is_monthly_member = None
        is_yearly_member = None
        l_hours_remaining = None

        # Common for all members views ===================================================
        l_categories = Category.objects.all()
        l_attributes = Attribute.objects.all()
        try:
            logged_member = Member.objects.get(django_user__username=request.user)
            show_describe_button = logged_member.is_editor(request)
            is_monthly_member = logged_member.is_monthly_member()
            is_yearly_member = logged_member.is_yearly_member()

            if logged_member.is_monthly_member() is True or logged_member.is_yearly_member() is True:
                max_interactions = FIND_NEW_FRIENDS_MAX_MEMBER_DAILY_INTERACTIONS
            else:
                max_interactions = FIND_NEW_FRIENDS_MAX_NON_MEMBER_DAILY_INTERACTIONS

            l_used_new_friends_limit = logged_member.new_friends_in_last_day
            l_new_friends_remaining = max_interactions - l_used_new_friends_limit

            l_new_friends_in_last_day_interval_start = logged_member.new_friends_in_last_day_interval_start
            if l_new_friends_in_last_day_interval_start:
                l_time_remaining = timezone.now() - l_new_friends_in_last_day_interval_start
                days, seconds = l_time_remaining.days, l_time_remaining.seconds
                l_hours_remaining = abs(days) * 24 + seconds // 3600
                l_hours_remaining = FIND_FRIENDS_LIMIT_PERIOD_RESET_TIME_DAYS * 24 - l_hours_remaining
            else:
                l_hours_remaining = None
        except ObjectDoesNotExist:
            logged_member = None
        except:
            raise

        # load members categories
        l_member_categories = MemberBelongsToCategory.objects.filter(instagram_user=logged_member).values('category')
        l_member_attributes = MemberBelongsToAttribute.objects.filter(instagram_user=logged_member).values('attribute')

        l_followers_set = Follower.objects.filter(inspiringuser__isnull=False,
                                                  is_user_active=True,
                                                  deactivated_by_mod=False
                                                  ).exclude(member=logged_member).order_by('interaction_count')

        l_followers_categories = FollowerBelongsToCategory.objects.\
            filter(category=l_member_categories, instagram_user=l_followers_set).values('instagram_user')

        l_followers_attributes = FollowerBelongsToAttribute.objects.\
            filter(attribute=l_member_attributes, instagram_user=l_followers_set).values('instagram_user')

        l_new_friends_list = []
        for follower_category in l_followers_categories:
            if follower_category in l_followers_attributes:
                l_new_friends_list.extend([follower_category[u'instagram_user']])

        l_followers_set_filtered = Follower.objects.filter(id__in=l_new_friends_list).order_by('interaction_count')

        if l_new_friends_remaining > 10:
            l_followers_set_filtered = l_followers_set_filtered[:10] # Get a number of new friends form membership level
        else:
            l_followers_set_filtered = l_followers_set_filtered[:l_new_friends_remaining] # Get a number of new friends form membership level

        l_token = logged_member.get_member_token(request)
        instagram_session = InstagramSession(p_is_admin=False, p_token=l_token['access_token'])
        instagram_session.init_instagram_API()

        l_friends_and_photos = []
        for follower in l_followers_set_filtered:
            l_best_photos = BestPhotos(
                instgram_user_id=follower.instagram_user_id,
                top_n_photos=FRIENDS_FIND_TOP_N_PHOTOS,
                search_photos_amount=FRIENDS_SEARCH_N_PHOTOS,
                instagram_api=instagram_session
            )
            l_best_photos.get_instagram_photos()
            l_best_photos.get_top_photos()
            l_top_photos_list = []
            for photo in l_best_photos.top_photos_list:
                l_instagram_photo = instagram_session.get_instagram_photo_info(photo[0])
                l_top_photos_list.extend([l_instagram_photo])
            l_friends_and_photos.append([follower, l_top_photos_list])


            for x_media in l_best_photos.top_photos_list:
                my_likes = MyLikes(request.user.username, x_media[0], instagram_session )
                has_user_liked_media, no_of_likes = my_likes.has_user_liked_media()
                if has_user_liked_media:
                    liked_photos.extend([x_media[0]])
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
                          friends_and_photos=l_friends_and_photos,
                          show_describe_button=show_describe_button,
                          new_friends_interaction=1,
                          max_interactions=max_interactions,
                          interactions_remaining=l_new_friends_remaining,
                          hours_remaining=l_hours_remaining,
                          liked_photos=liked_photos,

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


class InspiringUserIndexAllView(TemplateView):
    """
    display list of all inspiring artists on Squaresensor with stats
    """

    template_name = 'instagramuser/index-all-inspiring-artists.html'

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
        l_member_has_categories = False
        try:
            logged_member = Member.objects.get(django_user__username=request.user)
            show_describe_button = logged_member.is_editor(request)
            is_monthly_member = logged_member.is_monthly_member()
            is_yearly_member = logged_member.is_yearly_member()
            l_members_categories = MemberBelongsToCategory.objects.filter(instagram_user=logged_member)
            if len(l_members_categories) > 0:
                l_member_has_categories = True
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
        l_inspiring_users_queryset = InspiringUser.objects.all().order_by('instagram_user_name')

        l_inspiring_users_list = []
        for inspiring_user in l_inspiring_users_queryset:
            l_inspiring_user_categories = InspiringUserBelongsToCategory.objects.filter(instagram_user=inspiring_user)
            l_inspiring_user_attributes = InspiringUserBelongsToAttribute.objects.filter(instagram_user=inspiring_user)

            l_inspiring_user_categories_list = []
            for category in l_inspiring_user_categories:
                l_inspiring_user_categories_list.extend([category.category.title])

            l_inspiring_user_attributes_list = []
            for attribute in l_inspiring_user_attributes:
                l_inspiring_user_attributes_list.extend([attribute.attribute.title])

            l_inspiring_users_list.append([inspiring_user, l_inspiring_user_categories_list, l_inspiring_user_attributes_list])


        return render(request,
                      self.template_name,
                      dict(
                          inspiring_users_list=l_inspiring_users_list,
                          member_has_categories=l_member_has_categories,

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



class NewFriendsProcessingView(TemplateView):
    """
    display list of all inspiring artists on Squaresensor with stats
    """

    template_name = 'instagramuser/new-friends-processing.html'

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
            is_monthly_member = logged_member.is_monthly_member()
            is_yearly_member = logged_member.is_yearly_member()
        except ObjectDoesNotExist:
            logged_member = None
        except:
            raise HttpResponseNotFound

        # END Limit calculation ----------------------------------------------------------
        # END Common for all members views ===============================================
        test_app = TEST_APP
        l_inspiring_users_queryset = InspiringUser.objects.all().order_by('times_processed_for_friends', 'instagram_user_name')

        l_inspiring_users_list = []
        for inspiring_user in l_inspiring_users_queryset:
            l_inspiring_user_categories = InspiringUserBelongsToCategory.objects.filter(instagram_user=inspiring_user)
            l_inspiring_user_attributes = InspiringUserBelongsToAttribute.objects.filter(instagram_user=inspiring_user)

            l_inspiring_users_list.append([inspiring_user,
                                           len(l_inspiring_user_categories),
                                           len(l_inspiring_user_attributes),
                                           inspiring_user.times_processed_for_friends
            ]
            )

        # Limit calculation --------------------------------------------------------------
        x_ratelimit_remaining, x_ratelimit = logged_member.refresh_api_limits(request)


        x_ratelimit_used = x_ratelimit - x_ratelimit_remaining
        if x_ratelimit != 0:
            x_limit_pct = (x_ratelimit_used / x_ratelimit) * 100
        else:
            x_limit_pct = 100
        # END Limit calculation ----------------------------------------------------------
        # END Common for all members views ===============================================
        return render(request,
                      self.template_name,
                      dict(
                          inspiring_users_list=l_inspiring_users_list,
                          test_app=test_app,

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


class SuggestedInspiringUserIndexAllView(TemplateView):
    """
    Index view, displays list of categories
    """
    template_name = 'instagramuser/suggested-inspiring-artists.html'

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
            is_monthly_member = logged_member.is_monthly_member()
            is_yearly_member = logged_member.is_yearly_member()
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

        l_members_categories = \
            MemberBelongsToCategory.objects.filter(instagram_user=logged_member).select_related('category').values('category')
        l_members_categories_len = len(l_members_categories)
        l_members_attributes = \
            MemberBelongsToAttribute.objects.filter(instagram_user=logged_member).select_related('attribute').values('attribute')
        l_members_attributes_len = len(l_members_attributes)
        l_members_categories_and_attributes_len = l_members_categories_len + l_members_attributes_len
        l_inspiring_users_belong_to_categories = \
            InspiringUserBelongsToCategory.objects.filter(category__in=l_members_categories).select_related('instagram_user').values('instagram_user')

        l_inspiring_users_list = []
        l_inspiring_users = InspiringUser.objects.filter(id__in=l_inspiring_users_belong_to_categories)

        for inspiring_user in l_inspiring_users:
            weight = 0
            weight_atr = 0
            weight = InspiringUserBelongsToCategory.objects.filter(category__in=l_members_categories, instagram_user=inspiring_user).count()
            weight_atr = InspiringUserBelongsToAttribute.objects.filter(attribute__in=l_members_attributes, instagram_user=inspiring_user).count()
            pct_weight = 0
            if l_members_categories_and_attributes_len != 0:
                pct_weight = (weight + weight_atr) / l_members_categories_and_attributes_len * 100
            l_inspiring_users_list.append([inspiring_user, weight + weight_atr, pct_weight])

        l_inspiring_users_list =  sorted(l_inspiring_users_list,key=lambda x: x[1], reverse=True)


        return render(request,
                      self.template_name,
                      dict(
                          inspiring_users=l_inspiring_users_list[:30],



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