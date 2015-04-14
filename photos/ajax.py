from __future__ import division
import json
from time import sleep
from datetime import timedelta
from django.utils import timezone

from django.http import HttpResponseNotFound
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datetime_safe import datetime, date
from django.utils.translation import ugettext as _
from emoji.models import Emoji
from social_auth.db.django_models import UserSocialAuth

from attributes.models import Attribute
from categories.models import Category
from instagramuser.models import FollowingBelongsToCategory, FollowerBelongsToCategory, InspiringUserBelongsToCategory, \
    FollowingBelongsToAttribute, FollowerBelongsToAttribute, InspiringUserBelongsToAttribute, Follower, \
    NewFriendContactedByMember
from members.models import Member, MemberBelongsToCategory, MemberBelongsToAttribute
from photos.models import Photo

from libs.instagram.tools import InstagramSession, InstagramUserAdminUtils, InstagramComments, MyLikes
from dajaxice.decorators import dajaxice_register

from squaresensor.settings.base import INSTAGRAM_COMMENTS_ALLOWED, TEST_APP, INSTAGRAM_LIKES_PER_HOUR_LIMIT, \
    INSTAGRAM_COMMENTS_PER_HOUR_LIMIT, TEST_APP_LIKE_PER_PERIOD_LIMIT, TEST_APP_COMMENT_PER_PERIOD_LIMIT, \
    INSTAGRAM_LIMIT_PERIOD_RESET_TIME_HOURS

__author__ = 'n.nikolic'

@dajaxice_register
def save_attributes_and_categories(req, form, p_photo_id):
    """
    AJAX procedure for adding new Inspiring user and getting top photos
    :param req:
    :param form:
    :return:
    """

    # Common for all members views ===================================================
    l_categories = Category.objects.all()
    l_attributes = Attribute.objects.all()
    try:
        logged_member = Member.objects.get(django_user__username=req.user)
        if logged_member.is_editor(req):
            show_describe_button = True
    except ObjectDoesNotExist:
        logged_member = None
    except:
        raise HttpResponseNotFound


    # END Common for all members views ===============================================

    try:
        photo = Photo.objects.get(id=p_photo_id)
    except ObjectDoesNotExist:
        photo = None
    except:
        raise

    if photo:
        for checkbox in form:
            # update attributes section -------------------------------------------------------------------------------
            if checkbox.find('categories') != -1:
                # category checkbox is on
                l_ids = checkbox[11:]
                l_photo_id_pos = l_ids.find('_')
                l_photo_id = l_ids[:l_photo_id_pos]
                l_category_id = l_ids[l_photo_id_pos+1:]

                try:
                    l_category = Category.objects.get(id=l_category_id)
                except ObjectDoesNotExist:
                    l_category = None
                except:
                    raise

                if l_category:
                    photo.photo_category.add(l_category)

                    if photo.member_id:
                        l_member = photo.member_id
                        try:
                            l_member_category_already_added = MemberBelongsToCategory.objects.get(
                                instagram_user=l_member,
                                category=l_category,
                                )
                            l_member_category_already_added.frequency += 1
                            l_member_category_already_added.save()
                        except ObjectDoesNotExist:
                            l_member_category_already_added = None

                        if not l_member_category_already_added:
                            l_member_category = MemberBelongsToCategory(
                                instagram_user=l_member,
                                category=l_category,
                                frequency=1
                            )
                            l_member_category.save()

                    if photo.following_id:
                        l_following = photo.following_id
                        try:
                            l_following_category_already_added = FollowingBelongsToCategory.objects.get(
                                instagram_user=l_following,
                                category=l_category,
                                )
                            l_following_category_already_added.frequency += 1
                            l_following_category_already_added.save()
                        except ObjectDoesNotExist:
                            l_following_category_already_added = None

                        if not l_following_category_already_added:
                            l_following_category = FollowingBelongsToCategory(
                                instagram_user=l_following,
                                category=l_category,
                                frequency=1
                            )
                            l_following_category.save()

                    if photo.friend_id:
                        l_follower = photo.friend_id
                        try:
                            l_follower_category_already_added = FollowerBelongsToCategory.objects.get(
                                instagram_user=l_follower,
                                category=l_category,
                                )
                            l_follower_category_already_added.frequency += 1
                            l_follower_category_already_added.save()
                        except ObjectDoesNotExist:
                            l_follower_category_already_added = None

                        if not l_follower_category_already_added:
                            l_follower_category = FollowerBelongsToCategory(
                                instagram_user=l_follower,
                                category=l_category,
                                frequency=1
                            )
                            l_follower_category.save()

                    if photo.inspiring_user_id:
                        l_inspiring_user = photo.inspiring_user_id
                        try:
                            l_inspiring_user_category_already_added = InspiringUserBelongsToCategory.objects.get(
                                instagram_user=l_inspiring_user,
                                category=l_category,
                                )
                            l_inspiring_user_category_already_added.frequency += 1
                            l_inspiring_user_category_already_added.save()
                        except ObjectDoesNotExist:
                            l_inspiring_user_category_already_added = None

                        if not l_inspiring_user_category_already_added:
                            l_inspiring_user_category = InspiringUserBelongsToCategory(
                                instagram_user=l_inspiring_user,
                                category=l_category,
                                frequency=1
                            )
                            l_inspiring_user_category.save()

                        #add photo to their good followers / new friends
                        l_followers = Follower.objects.filter(inspiringuser=l_inspiring_user)
                        if l_followers:
                            for follower in l_followers:
                                try:
                                    l_follower_category_already_added = FollowerBelongsToCategory.objects.get(
                                        instagram_user=follower,
                                        category=l_category,
                                        )
                                    l_follower_category_already_added.frequency += 1
                                    l_follower_category_already_added.save()
                                except ObjectDoesNotExist:
                                    l_follower_category_already_added = None

                                if not l_follower_category_already_added:
                                    l_followers_belong_to_category = \
                                        FollowerBelongsToCategory(
                                            instagram_user=follower,
                                            category=l_category,
                                            frequency=1
                                        )
                                    l_followers_belong_to_category.save()




            # update attributes section -------------------------------------------------------------------------------
            if checkbox.find('attributes') != -1:
                # attribute checkbox is on
                l_ids = checkbox[11:]
                l_photo_id_pos = l_ids.find('_')
                l_photo_id = l_ids[:l_photo_id_pos]
                l_attribute_id = l_ids[l_photo_id_pos+1:]

                try:
                    l_attribute = Attribute.objects.get(id=l_attribute_id)
                except ObjectDoesNotExist:
                    l_attribute = None
                except:
                    raise

                if l_attribute:
                    photo.photo_attribute.add(l_attribute)

                    if photo.member_id:
                        l_member = photo.member_id
                        try:
                            l_member_attribute_already_added = MemberBelongsToAttribute.objects.get(
                                instagram_user=l_member,
                                attribute=l_attribute,
                                )
                            l_member_attribute_already_added.frequency += 1
                            l_member_attribute_already_added.save()
                        except ObjectDoesNotExist:
                            l_member_attribute_already_added = None

                        if not l_member_attribute_already_added:
                            l_member_attribute = MemberBelongsToAttribute(
                                instagram_user=l_member,
                                attribute=l_attribute,
                                frequency=1
                            )
                            l_member_attribute.save()

                    if photo.following_id:
                        l_following = photo.following_id
                        try:
                            l_following_attribute_already_added = FollowingBelongsToAttribute.objects.get(
                                instagram_user=l_following,
                                attribute=l_attribute,
                                )
                            l_following_attribute_already_added.frequency += 1
                            l_following_attribute_already_added.save()
                        except ObjectDoesNotExist:
                            l_following_attribute_already_added = None

                        if not l_following_attribute_already_added:
                            l_following_attribute = FollowingBelongsToAttribute(
                                instagram_user=l_following,
                                attribute=l_attribute,
                                frequency=1
                            )
                            l_following_attribute.save()

                    if photo.friend_id:
                        l_follower = photo.friend_id
                        try:
                            l_follower_attribute_already_added = FollowerBelongsToAttribute.objects.get(
                                instagram_user=l_follower,
                                attribute=l_attribute,
                                )
                            l_follower_attribute_already_added.frequency += 1
                            l_follower_attribute_already_added.save()
                        except ObjectDoesNotExist:
                            l_follower_attribute_already_added = None

                        if not l_follower_attribute_already_added:
                            l_follower_attribute = FollowerBelongsToAttribute(
                                instagram_user=l_follower,
                                attribute=l_attribute,
                                frequency=1
                            )
                            l_follower_attribute.save()

                    if photo.inspiring_user_id:
                        l_inspiring_user = photo.inspiring_user_id
                        try:
                            l_inspiring_user_attribute_already_added = InspiringUserBelongsToAttribute.objects.get(
                                instagram_user=l_inspiring_user,
                                attribute=l_attribute,
                                )
                            l_inspiring_user_attribute_already_added.frequency += 1
                            l_inspiring_user_attribute_already_added.save()
                        except ObjectDoesNotExist:
                            l_inspiring_user_attribute_already_added = None

                        if not l_inspiring_user_attribute_already_added:
                            l_inspiring_user_attribute = InspiringUserBelongsToAttribute(
                                instagram_user=l_inspiring_user,
                                attribute=l_attribute,
                                frequency=1
                            )
                            l_inspiring_user_attribute.save()


                        #add photo to their good followers / new friends
                        l_followers = Follower.objects.filter(inspiringuser=l_inspiring_user)
                        if l_followers:
                            for follower in l_followers:
                                try:
                                    l_follower_attribute_already_added = FollowerBelongsToAttribute.objects.get(
                                        instagram_user=follower,
                                        attribute=l_attribute,
                                        )
                                    l_follower_attribute_already_added.frequency += 1
                                    l_follower_attribute_already_added.save()
                                except ObjectDoesNotExist:
                                    l_follower_attribute_already_added = None

                                if not l_follower_attribute_already_added:
                                    l_followers_belong_to_attribute = \
                                        FollowerBelongsToAttribute(
                                            instagram_user=follower,
                                            attribute=l_attribute,
                                            frequency=1
                                        )
                                    l_followers_belong_to_attribute.save()

    l_modal_name = '#myModal_%s' % (p_photo_id)
    # Limit calculation --------------------------------------------------------------
    logged_member.refresh_api_limits(req)
    x_ratelimit_remaining, x_ratelimit = logged_member.get_api_limits()

    x_ratelimit_used = x_ratelimit - x_ratelimit_remaining
    if x_ratelimit != 0:
        x_limit_pct = (x_ratelimit_used / x_ratelimit) * 100
    else:
        x_limit_pct = 100
    # END Limit calculation ----------------------------------------------------------

    return json.dumps({
        'modal_name': l_modal_name,
        }
    )

@dajaxice_register
def load_instagram_comments(req, p_photo_id, p_new_friends_interaction):
    """
    Load Instagram photos for Instagram photo p_photo_id, and return text to modal dialog
    :param req:
    :param p_photo_id:
    :return:
    """
    instagram_thumbnail_URL = None
    tokens = UserSocialAuth.get_social_auth_for_user(req.user).get().tokens
    ig_session = InstagramSession(p_is_admin=False, p_token=tokens['access_token'])
    ig_session.init_instagram_API()

    l_instagram_comments = InstagramComments(p_photo_id=p_photo_id, p_instagram_session=ig_session)
    l_comments, instagram_thumbnail_url, photo_caption = l_instagram_comments.get_all_comments()

    l_comments_list = l_instagram_comments.process_instagram_comments('thread', l_comments)

    #for comment in l_comments:
    #    comment.text = Emoji.replace_unicode(comment.text)

    html_text = render_to_string('photos/modal_comment_section.html',
                                 dict(
                                     comments=l_comments_list,
                                     p_photo_id=p_photo_id,
                                     instagram_thumbnail_url=instagram_thumbnail_url,
                                     photo_caption=photo_caption,
                                     p_new_friends_interaction=p_new_friends_interaction
                                     )
    )

    return json.dumps({
        'error': 0,
        'error_message': '',
        'html_text': html_text,
        'p_photo_id': p_photo_id,
        }
    )


@dajaxice_register
def send_instagram_comment(req, form, p_photo_id, p_inline, p_new_friends_interaction):
    """
    Send instagram comment
    :param req:
    :param form:
    :param p_photo_id:
    :return:
    """

    # Common for all members views ===================================================
    l_categories = Category.objects.all()
    l_attributes = Attribute.objects.all()
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

    l_instagram_photo = ig_session.get_instagram_photo_info(p_photo_id)
    l_photo_author_instagram_id = l_instagram_photo.user.id

    if p_inline == '':
        l_comment_form_input_id = u'new_comment_%s' %(p_photo_id)
    else:
        l_comment_form_input_id = u'new_comment_%s_%s' %(p_photo_id, p_inline)
    comment_text = form[l_comment_form_input_id]

    # checking number of comments in the last period
    l_comments_in_last_minute = logged_member.comments_in_last_minute
    l_comments_in_last_minute_interval_start = logged_member.comments_in_last_minute_interval_start

    l_timedelta = timedelta(hours=+INSTAGRAM_LIMIT_PERIOD_RESET_TIME_HOURS)

    if l_comments_in_last_minute_interval_start:
        #l_likes_in_last_minute_interval_end = l_likes_in_last_minute_interval_start + timedelta(hours=+1)
        l_diff = l_comments_in_last_minute_interval_start - timezone.now()
        if l_diff > l_timedelta:
            #hour has passed - reset the counters
            logged_member.comments_in_last_minute = 0
            logged_member.comments_in_last_minute_interval_start = timezone.now()
            logged_member.save()
            l_comments_in_last_minute = 0

    else:
        logged_member.comments_in_last_minute = 1
        logged_member.comments_in_last_minute_interval_start = timezone.now()
        logged_member.save()
        l_comments_in_last_minute = 1



    if TEST_APP:
        l_instagram_comments_per_hour_limit = TEST_APP_COMMENT_PER_PERIOD_LIMIT
    else:
        l_instagram_comments_per_hour_limit = INSTAGRAM_COMMENTS_PER_HOUR_LIMIT

    l_instagram_comments = InstagramComments(p_photo_id=p_photo_id, p_instagram_session=ig_session)
    if logged_member.comments_in_last_minute < l_instagram_comments_per_hour_limit:
        if INSTAGRAM_COMMENTS_ALLOWED == '1':
            l_result = l_instagram_comments.send_instagram_comment(p_comment_text=comment_text)
            l_comments_in_last_minute += 1
            logged_member.comments_in_last_minute = l_comments_in_last_minute
            logged_member.save()
        else:
            l_comments_in_last_minute += 1
            logged_member.comments_in_last_minute = l_comments_in_last_minute
            logged_member.save()
            l_result = 'notallowed'
    else:
        l_result = 'limit'

    if (p_new_friends_interaction == 1):
        try:
            l_interacted_friend = Follower.objects.get(instagram_user_id=l_photo_author_instagram_id)
        except ObjectDoesNotExist:
            l_interacted_friend = None
        except:
            raise

        if l_interacted_friend:
            l_interacted_friend.member.add(logged_member)
            l_interacted_friend.interaction_count += 1
            l_interacted_friend.save()
            # increase member daily interactions count
            l_today = timezone.now().date()
            if l_today == logged_member.daily_new_friends_interactions_date:
                logged_member.daily_new_friends_interactions += 1
            else:
                logged_member.daily_new_friends_interactions_date = l_today
                logged_member.daily_new_friends_interactions = 1
            logged_member.save()

            l_new_friend_contacted = NewFriendContactedByMember(
                member=logged_member,
                friend=l_interacted_friend,
                contact_date=timezone.now(),
                contact_count=1,
                interaction_type='C'
            )
            l_new_friend_contacted.save()


    l_comments_count = l_instagram_comments.get_comments_count()

    # Limit calculation --------------------------------------------------------------
    x_ratelimit_remaining, x_ratelimit = logged_member.get_api_limits()

    x_ratelimit_used = x_ratelimit - x_ratelimit_remaining
    if x_ratelimit != 0:
        x_limit_pct = (x_ratelimit_used / x_ratelimit) * 100
    else:
        x_limit_pct = 100
    # END Limit calculation ----------------------------------------------------------
    # END Common for all members views ===============================================



    return json.dumps(
        dict(p_photo_id=p_photo_id,
             l_comments_count=l_comments_count,
             p_new_friends_interaction=p_new_friends_interaction,
             p_photo_author_instagram_id=l_photo_author_instagram_id,
             result=l_result,

             x_ratelimit_remaining=x_ratelimit_remaining,
             x_ratelimit=x_ratelimit,
             x_limit_pct=x_limit_pct,
             comments_per_minute=l_comments_in_last_minute,
             )
    )


@dajaxice_register
def like_instagram_picture(req, p_photo_id):
    """

    :param req:
    :type req:
    :param form:
    :type form:
    :param p_photo_id:
    :type p_photo_id:
    :param p_inline:
    :type p_inline:
    :return:
    :rtype:
    """

    # Common for all members views ===================================================
    l_categories = Category.objects.all()
    l_attributes = Attribute.objects.all()
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

    l_my_likes = MyLikes(p_instgram_user = logged_member.instagram_user_name,
                         p_photo_id = p_photo_id,
                         p_instagram_api= ig_session)



    # Limit calculation --------------------------------------------------------------
    logged_member.refresh_api_limits(req)
    x_ratelimit_remaining, x_ratelimit = logged_member.get_api_limits()

    x_ratelimit_used = x_ratelimit - x_ratelimit_remaining
    if x_ratelimit != 0:
        x_limit_pct = (x_ratelimit_used / x_ratelimit) * 100
    else:
        x_limit_pct = 100
    # END Limit calculation ----------------------------------------------------------
    # END Common for all members views ===============================================
    sleep(0.5)
    x, no_of_likes = l_my_likes.has_user_liked_media()

    #Todo check likes per minute
    l_likes_in_last_minute = logged_member.likes_in_last_minute
    l_likes_in_last_minute_interval_start = logged_member.likes_in_last_minute_interval_start
    l_timedelta = timedelta(hours=+INSTAGRAM_LIMIT_PERIOD_RESET_TIME_HOURS)

    if l_likes_in_last_minute_interval_start:
        #l_likes_in_last_minute_interval_end = l_likes_in_last_minute_interval_start + timedelta(hours=+1)
        l_diff = l_likes_in_last_minute_interval_start - timezone.now()
        if l_diff > l_timedelta:
            #hour has passed - reset the counters
            logged_member.likes_in_last_minute = 0
            logged_member.likes_in_last_minute_interval_start = timezone.now()
            logged_member.save()
            l_likes_in_last_minute = 0
        else:
            l_likes_in_last_minute += 1
            logged_member.likes_in_last_minute = l_likes_in_last_minute
            logged_member.save()
    else:
        logged_member.likes_in_last_minute = 1
        logged_member.likes_in_last_minute_interval_start = timezone.now()
        logged_member.save()
        l_likes_in_last_minute = 1

    if TEST_APP:
        l_instagram_likes_per_hour_limit = TEST_APP_LIKE_PER_PERIOD_LIMIT
    else:
        l_instagram_likes_per_hour_limit = INSTAGRAM_LIKES_PER_HOUR_LIMIT

    if logged_member.likes_in_last_minute < l_instagram_likes_per_hour_limit:
        result = l_my_likes.like_instagram_media()
    else:
        result = 'limit'

    return json.dumps(
        dict(p_photo_id=p_photo_id,
             result=result,
             no_of_likes=no_of_likes,

             x_ratelimit_remaining=x_ratelimit_remaining,
             x_ratelimit=x_ratelimit,
             x_limit_pct=x_limit_pct,
             likes_per_minute=l_likes_in_last_minute,
             )
    )