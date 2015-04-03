import json

from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _

from dajaxice.decorators import dajaxice_register
from attributes.models import Attribute
from categories.models import Category
from members.models import Member, MemberBelongsToCategory, MemberBelongsToAttribute

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