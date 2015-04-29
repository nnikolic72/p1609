from __future__ import absolute_import
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datetime_safe import datetime

from celery import shared_task
from celery.contrib import rdb
from libs.instagram.tools import InstagramSession, BestPhotos
from smartfeed.models import SquareFollowing, SquareFollowingMember

__author__ = 'n.nikolic'

@shared_task
def smart_feed_subscribe_task(p_instagram_user_id, p_color, l_token, l_logged_member_id):

    ig_session = InstagramSession(p_is_admin=False, p_token=l_token)
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

        # l_token = logged_member.get_member_token(req)
        instagram_session = InstagramSession(p_is_admin=False, p_token=l_token)
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
        member_id=l_logged_member_id).exists()

    if l_new_squarefollowing_check:
        try:
            l_existing_squarefollowing_members_level = SquareFollowingMember.objects.get(
                squarefollowing=l_squarefollowing,
                member_id=l_logged_member_id)
        except ObjectDoesNotExist:
            l_existing_squarefollowing_members_level = None
        except:
            raise

        if l_squarefollowing_level != l_existing_squarefollowing_members_level.squarefollowing_level:
            SquareFollowingMember.objects.filter(
                squarefollowing=l_squarefollowing,
                member_id=l_logged_member_id).delete()

            l_new_squarefollowing_members = SquareFollowingMember(
                squarefollowing=l_squarefollowing,
                member_id=l_logged_member_id,
                squarefollowing_level=l_squarefollowing_level
            )
            l_new_squarefollowing_members.save()
    else:
        l_new_squarefollowing_members = SquareFollowingMember(
            squarefollowing=l_squarefollowing,
            member_id=l_logged_member_id,
            squarefollowing_level=l_squarefollowing_level
        )
        l_new_squarefollowing_members.save()

    action_result = 1