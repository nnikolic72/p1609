import json

from dajaxice.decorators import dajaxice_register
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.template.loader import render_to_string
from social_auth.db.django_models import UserSocialAuth
from instagramuser.models import InspiringUser
from libs.instagram.tools import BestFollowings, InstagramSession
from members.models import Member
from .models import SquareFollowing
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
        if not SquareFollowing.objects\
                .filter(instagram_user_name=following.username, member_id=logged_member)\
                .exists():
            # There is no following in SquareFollowings
            is_inspiring_user = False
            if InspiringUser.objects\
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
    if p_color == 'green':
        l_new_squarefollowing.squarefollowing_level = SquareFollowing.G
    if p_color == 'yellow':
        l_new_squarefollowing.squarefollowing_level = SquareFollowing.Y
    if p_color == 'red':
        l_new_squarefollowing.squarefollowing_level = SquareFollowing.R
    l_new_squarefollowing.save()
    l_new_squarefollowing.member_id.add(logged_member)
    action_result = 1

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
             action_result=action_result,
             p_instagram_user_id=p_instagram_user_id,
             p_color=p_color,

             x_ratelimit_remaining=x_ratelimit_remaining,
             x_ratelimit=x_ratelimit,
             x_limit_pct=x_limit_pct,
             )
    )