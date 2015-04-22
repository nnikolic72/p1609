from __future__ import division
import json
from datetime import timedelta
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.utils.datetime_safe import datetime
from django.utils.translation import ugettext as _

from dajaxice.decorators import dajaxice_register
from attributes.models import Attribute
from categories.models import Category
from libs.instagram.tools import update_member_limits_f
from members.models import Member, MemberBelongsToCategory, MemberBelongsToAttribute
from squaresensor.settings.base import TEST_APP

__author__ = 'n.nikolic'

@dajaxice_register
def select_member_category(req, p_category_id, p_logged_member_id):
    """

    :param req:
    :type req:
    :param p_category_id:
    :type p_category_id:
    :param p_logged_member_id:
    :type p_logged_member_id:
    :return:
    :rtype:
    """

    result = None

    try:
        l_logged_member = Member.objects.get(id=p_logged_member_id)
    except ObjectDoesNotExist:
        l_logged_member = None

    try:
        l_category = Category.objects.get(id=p_category_id)
    except ObjectDoesNotExist:
        l_category = None

    if l_logged_member and l_category:
        try:
            l_member_in_category = MemberBelongsToCategory.objects.get(
                instagram_user=l_logged_member,
                category=l_category
            )
        except ObjectDoesNotExist:
            l_member_in_category = None

        if not l_member_in_category:
            # Member is not in category - add
            l_member_in_category_add = MemberBelongsToCategory(
                instagram_user=l_logged_member,
                category=l_category,
                frequency=1
            )
            l_member_in_category_add.save()
            result = 'add'
        else:
            # Member is in category - remove it
            l_member_in_category.delete()
            result = 'remove'

    return json.dumps(
        dict(p_category_id=p_category_id,
             p_result=result,
             )
    )

@dajaxice_register
def squaresensor_wizard_complete(req):
    try:
        logged_member = Member.objects.get(django_user__username=req.user)
        logged_member.help_first_time_wizard = False
        logged_member.help_first_time_wizard_cur_step = 4
        logged_member.save()
    except ObjectDoesNotExist:
        logged_member = None

    return json.dumps(
        dict(
             )
    )

@dajaxice_register
def squaresensor_wizard(req, p_current_step):
    """

    :param req:
    :type req:
    :param p_category_id:
    :type p_category_id:
    :param p_logged_member_id:
    :type p_logged_member_id:
    :return:
    :rtype:
    """

    result = 'error'
    l_current_step = None
    l_next_step = None

    try:
        logged_member = Member.objects.get(django_user__username=req.user)

        l_likes_in_last_minute, l_comments_in_last_minute = update_member_limits_f(req, logged_member)
        show_describe_button = logged_member.is_editor(req)
        # instagram_user = Member.objects.get(django_user__username=request.user)
        is_monthly_member = logged_member.is_monthly_member()
        is_yearly_member = logged_member.is_yearly_member()
        queryset = Member.objects.filter(django_user__username=req.user)


        logged_member.help_first_time_wizard_cur_step = p_current_step
        l_current_step = int(logged_member.help_first_time_wizard_cur_step)
        l_next_step = l_current_step + 1

    except ObjectDoesNotExist:
        logged_member = None

    html_text = None

    if p_current_step == '1':
        l_categories = Category.objects.all()

        html_text = render_to_string('members/wizard-s1-html.html',
                                     dict(
                                         categories=l_categories,
                                         logged_member=logged_member,
                                         current_step=l_current_step,
                                         next_step=l_next_step,
                                         p_instagram_user_id=logged_member.instagram_user_id,
                                     )
        )
        result = 'ok'

    if p_current_step == '2':
        l_attributes = Attribute.objects.all()

        html_text = render_to_string('members/wizard-s2-html.html',
                                     dict(
                                         attributes=l_attributes,
                                         logged_member=logged_member,
                                         current_step=l_current_step,
                                         next_step=l_next_step,
                                         p_instagram_user_id=logged_member.instagram_user_id,
                                     )
        )
        result = 'ok'

    if p_current_step == '3':

        html_text = render_to_string('members/wizard-s3-html.html',
                                     dict(

                                         logged_member=logged_member,
                                         current_step=l_current_step,
                                         next_step=l_next_step,
                                         p_instagram_user_id=logged_member.instagram_user_id,
                                     )
        )
        result = 'ok'

    if p_current_step == '4':
        logged_member.help_first_time_wizard = False
        logged_member.help_first_time_wizard_cur_step = 4
        logged_member.save()
        #return HttpResponseRedirect(reverse("members:dashboard"))

    return json.dumps(
        dict(p_current_step=p_current_step,
             html_text=html_text,
             p_result=result,
             status=result,
             p_instagram_user_id=logged_member.instagram_user_id,
             )
    )


@dajaxice_register
def squaresensor_wizard_increase_step(req, p_current_step):
    """

    :param req:
    :type req:
    :param p_category_id:
    :type p_category_id:
    :param p_logged_member_id:
    :type p_logged_member_id:
    :return:
    :rtype:
    """

    result = 'error'
    l_current_step = None
    l_next_step = None

    try:
        logged_member = Member.objects.get(django_user__username=req.user)


        logged_member.help_first_time_wizard_cur_step = p_current_step
        l_current_step = int(logged_member.help_first_time_wizard_cur_step)
        l_next_step = l_current_step + 1
        logged_member.help_first_time_wizard_cur_step = str(l_next_step)
        logged_member.save()

    except ObjectDoesNotExist:
        logged_member = None



    return json.dumps(
        dict(
             )
    )

@dajaxice_register
def select_member_attribute(req, p_attribute_id, p_logged_member_id):
    """

    :param req:
    :type req:
    :param p_attribute_id:
    :type p_attribute_id:
    :param p_logged_member_id:
    :type p_logged_member_id:
    :return:
    :rtype:
    """

    result = None

    try:
        l_logged_member = Member.objects.get(id=p_logged_member_id)
    except ObjectDoesNotExist:
        l_logged_member = None

    try:
        l_attribute = Attribute.objects.get(id=p_attribute_id)
    except ObjectDoesNotExist:
        l_attribute = None

    if l_logged_member and l_attribute:
        try:
            l_member_in_attribute = MemberBelongsToAttribute.objects.get(
                instagram_user=l_logged_member,
                attribute=l_attribute
            )
        except ObjectDoesNotExist:
            l_member_in_attribute = None

        if not l_member_in_attribute:
            # Member is not in category - add
            l_member_in_attribute_add = MemberBelongsToAttribute(
                instagram_user=l_logged_member,
                attribute=l_attribute,
                frequency=1
            )
            l_member_in_attribute_add.save()
            result = 'add'
        else:
            # Member is in category - remove it
            l_member_in_attribute.delete()
            result = 'remove'

    return json.dumps(
        dict(p_attribute_id=p_attribute_id,
             p_result=result,
             )
    )

@dajaxice_register
def check_members_limits(req):

    l_likes_in_last_minute = None
    l_comments_in_last_minute = None

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

    l_likes_in_last_minute, l_comments_in_last_minute = update_member_limits_f(req, logged_member)



    # END Common for all members views ===============================================

    # Limit calculation --------------------------------------------------------------
    #logged_member.get_api_limits(req)
    x_ratelimit_remaining, x_ratelimit = logged_member.get_api_limits()

    x_ratelimit_used = x_ratelimit - x_ratelimit_remaining
    if x_ratelimit != 0:
        x_limit_pct = (x_ratelimit_used / x_ratelimit) * 100
    else:
        x_limit_pct = 100
    # END Limit calculation ----------------------------------------------------------

    return json.dumps(
        dict(
            x_ratelimit_remaining=x_ratelimit_remaining,
            x_ratelimit=x_ratelimit,
            x_limit_pct=x_limit_pct,
            likes_in_last_minute=l_likes_in_last_minute,
            comments_in_last_minute=l_comments_in_last_minute,
            )
    )

@dajaxice_register
def dismiss_help(req, p_help_name):

    try:
        logged_member = Member.objects.get(django_user__username=req.user)
        if logged_member.is_editor(req):
            show_describe_button = True
    except ObjectDoesNotExist:
        logged_member = None
    except:
        raise HttpResponseNotFound

    if p_help_name == 'help_members_dashboard':
        logged_member.help_members_dashboard = False
        logged_member.save()

    if p_help_name == 'help_members_commenter':
        logged_member.help_members_commenter = False
        logged_member.save()

    if p_help_name == 'help_photos_modal_comment_section':
        logged_member.help_photos_modal_comment_section = False
        logged_member.save()

    if p_help_name == 'help_photos_allbest':
        logged_member.help_photos_allbest = False
        logged_member.save()

    if p_help_name == 'help_smartfeed_index':
        logged_member.help_smartfeed_index = False
        logged_member.save()

    if p_help_name == 'help_smartfeed_configure':
        logged_member.help_smartfeed_configure = False
        logged_member.save()

    if p_help_name == 'help_instagramuser_find_new_friends':
        logged_member.help_instagramuser_find_new_friends = False
        logged_member.save()

    if p_help_name == 'help_instagramuser_index_inspiring_artists2':
        logged_member.help_instagramuser_index_inspiring_artists2 = False
        logged_member.save()

    if p_help_name == 'help_categories_index':
        logged_member.help_categories_index = False
        logged_member.save()

    if p_help_name == 'help_attributes_index':
        logged_member.help_attributes_index = False
        logged_member.save()


    if p_help_name == 'help_reserved1':
        logged_member.help_reserved1 = False
        logged_member.save()

    if p_help_name == 'help_reserved2':
        logged_member.help_reserved2 = False
        logged_member.save()

    if p_help_name == 'help_reserved3':
        logged_member.help_reserved3 = False
        logged_member.save()

    if p_help_name == 'help_reserved4':
        logged_member.help_reserved4 = False
        logged_member.save()

    if p_help_name == 'help_reserved5':
        logged_member.help_reserved5 = False
        logged_member.save()

    return json.dumps(
        dict(

            )
    )