from __future__ import absolute_import

from celery import shared_task
from libs.instagram.tools import InstagramSession, MyLikes, InstagramComments

__author__ = 'n.nikolic'

@shared_task
def like_instagram_media_task(p_instagram_user_name, p_photo_id, p_token):
    """
    Async task to like Instagram media

    :param p_instagram_user_name:
    :type p_instagram_user_name:
    :param p_photo_id:
    :type p_photo_id:
    :param p_token:
    :type p_token:
    :return:
    :rtype:
    """
    result = 'error'
    ig_session = InstagramSession(p_is_admin=False, p_token=p_token)
    ig_session.init_instagram_API()

    l_my_likes = MyLikes(p_instgram_user=p_instagram_user_name,
                         p_photo_id=p_photo_id,
                         p_instagram_api=ig_session)
    if l_my_likes:
        result = l_my_likes.like_instagram_media()

    return result


@shared_task
def send_instagram_comment_task(p_photo_id, p_comment_text, p_token):
    """
    Async task to like Instagram media

    :param p_instagram_user_name:
    :type p_instagram_user_name:
    :param p_photo_id:
    :type p_photo_id:
    :param p_token:
    :type p_token:
    :return:
    :rtype:
    """
    result = 'error'
    ig_session = InstagramSession(p_is_admin=False, p_token=p_token)
    ig_session.init_instagram_API()

    l_instagram_comments = InstagramComments(p_photo_id=p_photo_id, p_instagram_session=ig_session)
    if l_instagram_comments:
        l_instagram_comments.send_instagram_comment(p_comment_text=p_comment_text)

