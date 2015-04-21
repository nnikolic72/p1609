from __future__ import division
import json

from django.http import HttpResponseNotFound
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.translation import ugettext as _

from libs.instagram.tools import InstagramSession, InstagramUserAdminUtils
from dajaxice.decorators import dajaxice_register

from members.models import Member
from photos.models import Photo
from categories.models import Category
from attributes.models import Attribute
from .forms import AddInspiringUserForm
from instagramuser.models import InspiringUser, Follower, NewFriendContactedByMember

__author__ = 'n.nikolic'

@dajaxice_register
def analyze_user(req, form):
    """
    AJAX procedure for adding new Inspiring user and getting top photos
    :param req:
    :param form:
    :return:
    """

    add_user_form = AddInspiringUserForm(form)
    l_photos_queryset = None
    show_describe_button = False

    if add_user_form.is_valid():
        instagram_user_name = add_user_form.cleaned_data[u'instagram_user_name']
        instagram_user_name = instagram_user_name.lower().strip()

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
        logged_member.refresh_api_limits(req)
        x_ratelimit_remaining, x_ratelimit = logged_member.get_api_limits()

        x_ratelimit_used = x_ratelimit - x_ratelimit_remaining
        if x_ratelimit != 0:
            x_limit_pct = (x_ratelimit_used / x_ratelimit) * 100
        else:
            x_limit_pct = 100
        # END Limit calculation ----------------------------------------------------------
        # END Common for all members views ===============================================

        inspiring_user_cnt = InspiringUser.objects.filter(instagram_user_name=instagram_user_name).count()

        if inspiring_user_cnt > 0:
            return json.dumps({
                'already_exists': 1,
                'error': 1,
                'error_message': 'Inspiring artist already exists in our database.',
                'html_text': 'Inspiring artist already exists in our database.',
                }
            )
        else:
            # add new user and their photos
            l_token = logged_member.get_member_token(req)
            instagram_session = InstagramSession(p_is_admin=False, p_token=l_token['access_token'])
            instagram_session.init_instagram_API()
            user_search = instagram_session.is_instagram_user_valid(instagram_user_name)
            if len(user_search) > 0:
                if user_search[0].username == instagram_user_name:
                    ig_utils = InstagramUserAdminUtils()
                    inspiring_user = InspiringUser(instagram_user_name=instagram_user_name,
                                                   to_be_processed_for_basic_info=True,
                                                   to_be_processed_for_photos=True)
                    if inspiring_user:
                        inspiring_user.save()
                        queryset = InspiringUser.objects.filter(instagram_user_name=instagram_user_name)
                        if queryset.count() > 0:
                            ig_utils.process_instagram_user(req, queryset)
                            l_photos_queryset = Photo.objects.filter(inspiring_user_id=inspiring_user).order_by('-photo_rating')

                            if l_photos_queryset.count() > 0:
                                ig_utils.process_photos_by_instagram_api(req, l_photos_queryset)
                                l_photos_queryset = Photo.objects.filter(inspiring_user_id=inspiring_user).order_by('-photo_rating')



                    else:
                        return json.dumps({

                            'already_exists': 0,
                            'error': 1,
                            'error_message': 'Can not add Inspiring user in the database at this time.',
                            'html_text': '<p>Can not add Inspiring user in the database at this time.</p>'
                        }
                        )
                else:
                    return json.dumps({

                        'already_exists': 0,
                        'error': 1,
                        'error_message': 'Inspiring user does not exists.',
                        'html_text': '<p>Inspiring user does not exists.</p>'
                    }
                    )
            else:
                return json.dumps({

                    'already_exists': 0,
                    'error': 1,
                    'error_message': 'Instagram user does not exist.',
                    'html_text': 'Instagram user does not exist.',
                    }
                )


    html_text = render_to_string('photos/photo_gallery.html',
                                 dict(
                                     photos=l_photos_queryset,
                                     show_describe_button=show_describe_button,
                                     categories=l_categories,
                                     attributes=l_attributes,
                                     )
    )

    return json.dumps({
        'already_exists': 0,
        'error': 0,
        'error_message': '',
        'html_text': html_text
    }
    )

@dajaxice_register
def skip_new_friend(req, p_instagram_user_id):
    """
    Skip new friend while trying to find new friends
    :param req:
    :type req:
    :param p_instagram_user_id:
    :type p_instagram_user_id:
    :return:
    :rtype:
    """

    try:
        logged_member = Member.objects.get(django_user__username=req.user)
        if logged_member.is_editor(req):
            show_describe_button = True
    except ObjectDoesNotExist:
        logged_member = None
    except:
        raise HttpResponseNotFound

    try:
        l_new_friend_to_skip = Follower.objects.get(instagram_user_id=p_instagram_user_id)
    except ObjectDoesNotExist:
        l_new_friend_to_skip = None
        result = 'notfound'
    except:
        raise

    if l_new_friend_to_skip:
        l_new_friend_to_skip.member.add(logged_member)
        l_new_interaction = NewFriendContactedByMember(
            member=logged_member,
            friend=l_new_friend_to_skip,
            contact_date=timezone.now(),
            contact_count=1,
            interaction_type='S'
        )
        l_new_interaction.save()
        result = 'skipped'

    return json.dumps({
        'p_instagram_user_id': p_instagram_user_id,
        'result': result,
        }
    )



@dajaxice_register
def remove_new_friend(req, p_instagram_user_id):
    """
    Remove new friend, by moderator only, while trying to find new friends
    :param req:
    :type req:
    :param p_instagram_user_id:
    :type p_instagram_user_id:
    :return:
    :rtype:
    """

    try:
        logged_member = Member.objects.get(django_user__username=req.user)
        if logged_member.is_editor(req):
            show_describe_button = True
    except ObjectDoesNotExist:
        logged_member = None
    except:
        raise HttpResponseNotFound

    try:
        l_new_friend_to_skip = Follower.objects.get(instagram_user_id=p_instagram_user_id)
        l_new_friend_to_skip.deactivated_by_mod = True
        l_new_friend_to_skip.save()
        result='removed'
    except ObjectDoesNotExist:
        l_new_friend_to_skip = None
        result = 'notfound'
    except:
        raise


    return json.dumps({
        'p_instagram_user_id': p_instagram_user_id,
        'result': result,
        }
    )