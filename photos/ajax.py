from attributes.models import Attribute
from categories.models import Category
from instagramuser.models import FollowingBelongsToCategory, FollowerBelongsToCategory, InspiringUserBelongsToCategory, \
    FollowingBelongsToAttribute, FollowerBelongsToAttribute, InspiringUserBelongsToAttribute
from members.models import Member, MemberBelongsToCategory, MemberBelongsToAttribute
from photos.models import Photo

__author__ = 'n.nikolic'
import json

from django.http import HttpResponseNotFound
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _

from libs.instagram.tools import InstagramSession, InstagramUserAdminUtils
from dajaxice.decorators import dajaxice_register





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

    l_modal_name = '#myModal_%s' % (p_photo_id)

    return json.dumps({
        'modal_name': l_modal_name,
        }
    )