from __future__ import division
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.utils import translation
from django.utils.translation import ugettext as _
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from attributes.models import Attribute
from categories.models import Category
from instagramuser.models import InspiringUser

from squaresensor.settings.base import IS_APP_LIVE
from .forms import AddInspiringUserForm
from members.models import Member
from photos.models import Photo

class AddInspiringUserView(TemplateView):
    """
    Add new Inspiring user
    """
    template_name = 'instagramuser/add.html'

    def get(self, request, *args, **kwargs):
        """
        Handle get request - display photos and all controls

        :param request:
        :type request:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """

        # Common for all members views ===================================================
        try:
            logged_member = Member.objects.get(django_user__username=request.user)
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

        form = AddInspiringUserForm()

        return render(request,
                      self.template_name,
                      dict(
                          form=form,

                          logged_member=logged_member,
                          x_ratelimit_remaining=x_ratelimit_remaining,
                          x_ratelimit=x_ratelimit,
                          x_limit_pct=x_limit_pct
                          )
        )


class AddInspiringUserByNameView(TemplateView):
    """
    Add inspiring user by name
    """


class InspiringUserIndexView(TemplateView):
    """
    List all inspiring users
    """

    template_name = 'instagramuser/index-inspiring-artists.html'

    def get(self, request, *args, **kwargs):
        """
        Handle get request - display photos and all controls

        :param request:
        :type request:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """

        # Common for all members views ===================================================
        l_categories = Category.objects.all()
        l_attributes = Attribute.objects.all()
        try:
            logged_member = Member.objects.get(django_user__username=request.user)
            show_describe_button = logged_member.is_editor(request)
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
        l_inspiring_users_queryset = InspiringUser.objects.all()

        return render(request,
                      self.template_name,
                      dict(
                          inspiring_users=l_inspiring_users_queryset,

                          logged_member=logged_member,
                          x_ratelimit_remaining=x_ratelimit_remaining,
                          x_ratelimit=x_ratelimit,
                          x_limit_pct=x_limit_pct,
                          categories=l_categories,
                          attributes=l_attributes,
                          )
        )



class InspiringUserNameView(TemplateView):
    pass

