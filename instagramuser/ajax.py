from django.http import HttpResponseNotFound
from libs.instagram.tools import InstagramSession, InstagramUserAdminUtils
from members.models import Member
from photos.models import Photo
from categories.models import Category
from attributes.models import Attribute

__author__ = 'n.nikolic'
import json
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _

from dajaxice.decorators import dajaxice_register

from .forms import AddInspiringUserForm
from instagramuser.models import InspiringUser

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

    if add_user_form.is_valid():
        instagram_user_name = add_user_form.cleaned_data[u'instagram_user_name']
        instagram_user_name = instagram_user_name.lower()

        # Common for all members views ===================================================
        try:
            logged_member = Member.objects.get(django_user__username=req.user)
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

        inspiring_user = InspiringUser.objects.filter(django_user__username=instagram_user_name).count()

        if inspiring_user:
            return json.dumps({
                'photos': None,
                'already_exists': 1,
                'error': 1,
                'error_message': 'Inspiring artist already exists in our database.',
                'categories': None,
                'attributes': None,
                }
            )
        else:
            # add new user and their photos
            l_token = logged_member.get_member_token(req)
            instagram_session = InstagramSession(p_is_admin=False, p_token=l_token['access_token'])
            instagram_session.init_instagram_API()
            user_search = instagram_session.is_instagram_user_valid(instagram_user_name)

            ig_utils = InstagramUserAdminUtils()
            inspiring_user = InspiringUser(instagram_user_name=instagram_user_name,
                                           to_be_processed_for_basic_info=True,
                                           to_be_processed_for_photos=True)
            if inspiring_user:
                inspiring_user.save()
                queryset = InspiringUser.objects.filter(instagram_user_name=instagram_user_name)
                if queryset:
                    ig_utils.process_instagram_user(req, queryset)
                    l_photos_queryset = Photo.objects.filter(inspiring_user_id=inspiring_user).order_by('-photo_rating')

                    if l_photos_queryset.count() > 0:
                        ig_utils.process_photos_by_instagram_api(req, l_photos_queryset)
                        l_photos_queryset = Photo.objects.filter(inspiring_user_id=inspiring_user).order_by('-photo_rating')

                        l_categories = Category.objects.all()
                        l_attributes = Attribute.objects.all()
            else:
                return json.dumps({
                    'photos': None,
                    'already_exists': 0,
                    'error': 1,
                    'error_message': 'Can not add Inspiring user in the database at this time.',
                    'categories': None,
                    'attributes': None,
                    }
                )

    return json.dumps({
        'photos': l_photos_queryset,
        'already_exists': 0,
        'error': 0,
        'error_message': '',
        'categories': l_categories,
        'attributes': l_attributes,
        }
    )