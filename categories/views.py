from __future__ import division
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.utils import translation
from django.utils.translation import ugettext as _
from django.views.generic import FormView
from django.views.generic.base import TemplateView


# Create your views here.
from attributes.models import Attribute
from categories.models import Category
from instagramuser.models import InspiringUserBelongsToCategory
from members.models import Member


class CategoryIndexView(TemplateView):
    """
    Index view, displays list of categories
    """

    template_name = 'categories/index.html'

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
        l_categories_queryset = Category.objects.all()

        l_categories_result_list = []
        for category in l_categories_queryset:
            l_inspiring_users_count = InspiringUserBelongsToCategory.objects.filter(category=category).count()
            l_categories_result_list.append([category.title,
                                             category.description,
                                             category.slug,
                                             l_inspiring_users_count
            ]
            )

        return render(request,
                      self.template_name,
                      dict(
                          categories_list=l_categories_result_list,

                          logged_member=logged_member,
                          x_ratelimit_remaining=x_ratelimit_remaining,
                          x_ratelimit=x_ratelimit,
                          x_limit_pct=x_limit_pct,
                          categories=l_categories,
                          attributes=l_attributes,
                          )
        )

class CategoryNameView(TemplateView):
    """
    Index view, displays list of categories
    """
    template_name = 'categories/by-name.html'

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

        category_name = kwargs['p_category_slug']

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