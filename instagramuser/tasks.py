from __future__ import absolute_import
from instagramuser.models import InspiringUser
from celery.contrib import rdb
from members.models import Member

__author__ = 'n.nikolic'

from celery import shared_task

from libs.instagram.tools import InstagramUserAdminUtils

@shared_task
def process_instagram_user(requestNone, inspiring_users_id_list, l_is_admin, l_token):

    instagram_utils = InstagramUserAdminUtils(l_is_admin, l_token)

    queryset = InspiringUser.objects.filter(instagram_user_id__in=inspiring_users_id_list)

    if instagram_utils:
        buf = instagram_utils.process_instagram_user(queryset)

@shared_task
def process_squaresensor_member(requestNone, inspiring_users_id_list, l_is_admin, l_token):

    instagram_utils = InstagramUserAdminUtils(l_is_admin, l_token)

    queryset = Member.objects.filter(instagram_user_id__in=inspiring_users_id_list)

    if instagram_utils:
        buf = instagram_utils.process_instagram_user(queryset)