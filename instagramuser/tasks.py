from __future__ import absolute_import
from instagramuser.models import InspiringUser

__author__ = 'n.nikolic'

from celery import shared_task

from libs.instagram.tools import InstagramUserAdminUtils

@shared_task
def process_instagram_user(request, inspiring_users_id_list):
    instagram_utils = InstagramUserAdminUtils()

    queryset = InspiringUser.objects.filter(instagram_user_id__in=inspiring_users_id_list)
    if instagram_utils:
        buf = instagram_utils.process_instagram_user(None, queryset)