import json

from dajaxice.decorators import dajaxice_register

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

    return json.dumps(
        dict(
             l_instagram_followings=l_instagram_followings,
             )
    )