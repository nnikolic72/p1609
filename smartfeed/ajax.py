from __future__ import division
import json

from dajaxice.decorators import dajaxice_register
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.template.loader import render_to_string
from django.utils.datetime_safe import datetime
from social_auth.db.django_models import UserSocialAuth
from instagramuser.models import InspiringUser
from libs.instagram.tools import BestFollowings, InstagramSession, BestPhotos
from members.models import Member
from .models import SquareFollowing, SquareFollowingMember
from squaresensor.settings.base import IMPORT_MAX_INSTAGRAM_FOLLOWINGS

__author__ = 'tanja'

@dajaxice_register
def import_instagram_followings(req, p_instagram_user_id):
    """
    Get Instagram followings for user p_instagram_user_id
    :param req:
    :type req:
    :param p_instagram_user_id:
    :type p_instagram_user_id:
    :return:
    :rtype:
    """
    l_instagram_followings = None

    # Common for all members views ===================================================
    try:
        logged_member = Member.objects.get(django_user__username=req.user)
        if logged_member.is_editor(req):
            show_describe_button = True
    except ObjectDoesNotExist:
        logged_member = None
    except:
        raise HttpResponseNotFound

    tokens = UserSocialAuth.get_social_auth_for_user(req.user).get().tokens
    ig_session = InstagramSession(p_is_admin=False, p_token=tokens['access_token'])
    ig_session.init_instagram_API()

    l_instagram_followings = BestFollowings(
        p_instgram_user_id=p_instagram_user_id,
        p_user_type='',
        p_analyze_n_photos=IMPORT_MAX_INSTAGRAM_FOLLOWINGS,
        p_instagram_api=ig_session
    )

    l_instagram_followings_list = l_instagram_followings.get_instagram_followings()

    l_instagram_followings_result = []
    for following in l_instagram_followings_list:
        if not SquareFollowing.objects \
                .filter(instagram_user_name=following.username, member_id2=logged_member) \
                .exists():
            # There is no following in SquareFollowings
            is_inspiring_user = False
            if InspiringUser.objects \
                    .filter(instagram_user_name=following.username).exists():
                is_inspiring_user = True
            l_instagram_followings_result.append([following, is_inspiring_user])


    html_text = render_to_string('smartfeed/import_instagram_followings.html',
                                 dict(
                                     l_instagram_followings=l_instagram_followings_result,
                                     )
    )

    # Limit calculation --------------------------------------------------------------
    x_ratelimit_remaining, x_ratelimit = logged_member.get_api_limits()

    x_ratelimit_used = x_ratelimit - x_ratelimit_remaining
    if x_ratelimit != 0:
        x_limit_pct = (x_ratelimit_used / x_ratelimit) * 100
    else:
        x_limit_pct = 100
    # END Limit calculation ----------------------------------------------------------

    return json.dumps(
        dict(
            html_text=html_text,

            x_ratelimit_remaining=x_ratelimit_remaining,
            x_ratelimit=x_ratelimit,
            x_limit_pct=x_limit_pct,
            )
    )


@dajaxice_register
def smart_feed_subscribe(req, p_instagram_user_id, p_color):
    """
    Subscribe member to a following Instagram account in specified "color"
    :param req:
    :type req:
    :param p_instagram_user_id:
    :type p_instagram_user_id:
    :param p_color:
    :type p_color:
    :return:
    :rtype:
    """

    action_result = 0

    # Common for all members views ===================================================
    try:
        logged_member = Member.objects.get(django_user__username=req.user)
        if logged_member.is_editor(req):
            show_describe_button = True
    except ObjectDoesNotExist:
        logged_member = None
    except:
        raise HttpResponseNotFound

    tokens = UserSocialAuth.get_social_auth_for_user(req.user).get().tokens
    ig_session = InstagramSession(p_is_admin=False, p_token=tokens['access_token'])
    ig_session.init_instagram_API()
    l_instagram_following = ig_session.get_instagram_user(p_instagram_user_id)

    l_squarefollowing = SquareFollowing.objects.filter(

        instagram_user_id=p_instagram_user_id,
        instagram_user_name=l_instagram_following.username
    )

    l_squarefollowing_level = None
    if p_color == 'green':
        l_squarefollowing_level = SquareFollowingMember.G
    if p_color == 'yellow':
        l_squarefollowing_level = SquareFollowingMember.Y
    if p_color == 'red':
        l_squarefollowing_level = SquareFollowingMember.R

    if l_squarefollowing.count() == 0:
        #create new SquareFollowing
        l_new_squarefollowing = SquareFollowing(

            instagram_user_id=p_instagram_user_id,
            instagram_user_name=l_instagram_following.username
        )
        l_new_squarefollowing.number_of_followers = l_instagram_following.counts[u'followed_by']
        l_new_squarefollowing.number_of_followings = l_instagram_following.counts[u'follows']
        l_new_squarefollowing.number_of_media = l_instagram_following.counts[u'media']
        #l_new_squarefollowing.instagram_user_name = l_instagram_following.username
        l_new_squarefollowing.instagram_user_full_name = l_instagram_following.full_name
        #l_new_squarefollowing.instagram_user_id = l_instagram_following.id
        l_new_squarefollowing.instagram_profile_picture_URL = l_instagram_following.profile_picture
        l_new_squarefollowing.instagram_user_bio = l_instagram_following.bio
        l_new_squarefollowing.instagram_user_website_URL = l_instagram_following.website
        l_new_squarefollowing.instagram_user_name_valid = True

        #calculate poly----------------------------------------
        instagram_user_name = l_instagram_following.username

        l_good_photos = None

        l_token = logged_member.get_member_token(req)
        instagram_session = InstagramSession(p_is_admin=False, p_token=l_token['access_token'])
        instagram_session.init_instagram_API()
        user_search = instagram_session.is_instagram_user_valid(instagram_user_name)

        if (len(user_search) > 0) and (user_search[0].username == instagram_user_name):
            l_instagram_user = instagram_session.get_instagram_user(user_search[0].id)

            l_best_photos = BestPhotos(
                instgram_user_id=l_instagram_user.id,
                top_n_photos=0,
                search_photos_amount=100,
                instagram_api=instagram_session
            )
            l_best_photos.get_instagram_photos()
            l_recent_media = l_best_photos.l_latest_photos

            l_top_photos = None
            if l_best_photos.l_user_has_photos:
                l_polynom, l_max_days, l_min_days, l_max_likes, l_min_likes = l_best_photos.get_top_photos()

                l_new_squarefollowing.poly_theta_0 = l_polynom.coeffs[2]
                l_new_squarefollowing.poly_theta_1 = l_polynom.coeffs[1]
                l_new_squarefollowing.poly_theta_2 = l_polynom.coeffs[0]
                l_new_squarefollowing.poly_min_days = l_min_days
                l_new_squarefollowing.poly_max_days = l_max_days
                l_new_squarefollowing.poly_min_likes = l_min_likes
                l_new_squarefollowing.poly_max_likes = l_max_likes
                l_new_squarefollowing.poly_order = 2
                l_new_squarefollowing.times_processed = 1
                l_new_squarefollowing.last_processed = datetime.today()

        l_new_squarefollowing.save()
        l_squarefollowing = l_new_squarefollowing
    else:
        try:
            l_squarefollowing = SquareFollowing.objects.get(

                instagram_user_id=p_instagram_user_id,
                instagram_user_name=l_instagram_following.username
            )
        except ObjectDoesNotExist:
            l_squarefollowing = None
        except:
            raise

    # check if already following
    l_new_squarefollowing_check = SquareFollowingMember.objects.filter(
        squarefollowing=l_squarefollowing,
        member=logged_member).exists()

    if l_new_squarefollowing_check:
        try:
            l_existing_squarefollowing_members_level = SquareFollowingMember.objects.get(
                squarefollowing=l_squarefollowing,
                member=logged_member)
        except ObjectDoesNotExist:
            l_existing_squarefollowing_members_level = None
        except:
            raise

        if l_squarefollowing_level != l_existing_squarefollowing_members_level.squarefollowing_level:
            SquareFollowingMember.objects.filter(
                squarefollowing=l_squarefollowing,
                member=logged_member).delete()

            l_new_squarefollowing_members = SquareFollowingMember(
                squarefollowing=l_squarefollowing,
                member=logged_member,
                squarefollowing_level=l_squarefollowing_level
            )
            l_new_squarefollowing_members.save()
    else:
        l_new_squarefollowing_members = SquareFollowingMember(
            squarefollowing=l_squarefollowing,
            member=logged_member,
            squarefollowing_level=l_squarefollowing_level
        )
        l_new_squarefollowing_members.save()

    action_result = 1

    # Limit calculation --------------------------------------------------------------
    logged_member.refresh_api_limits(req)
    x_ratelimit_remaining, x_ratelimit = logged_member.get_api_limits()

    x_ratelimit_used = x_ratelimit - x_ratelimit_remaining
    if x_ratelimit != 0:
        x_limit_pct = (x_ratelimit_used / x_ratelimit) * 100
    else:
        x_limit_pct = 100
    # END Limit calculation ----------------------------------------------------------

    return json.dumps(
        dict(
            action_result=action_result,
            p_instagram_user_id=p_instagram_user_id,
            p_color=p_color,

            x_ratelimit_remaining=x_ratelimit_remaining,
            x_ratelimit=x_ratelimit,
            x_limit_pct=x_limit_pct,
            )
    )