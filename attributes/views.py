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
from instagramuser.models import InspiringUserBelongsToAttribute, InspiringUser
from members.models import Member


class AttributeIndexView(TemplateView):
    """
    Index view, displays list of attributes
    """

    template_name = 'attributes/index.html'

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
            is_monthly_member = logged_member.is_monthly_member()
            is_yearly_member = logged_member.is_yearly_member()
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
        l_attributes_queryset = Attribute.objects.all()

        l_attributes_result_list = []
        for attribute in l_attributes_queryset:
            l_inspiring_users_count = InspiringUserBelongsToAttribute.objects.filter(attribute=attribute).count()
            l_attributes_result_list.append([attribute.title,
                                             attribute.description,
                                             attribute.slug,
                                             l_inspiring_users_count
            ]
            )

        return render(request,
                      self.template_name,
                      dict(
                          attributes_list=l_attributes_result_list,

                          is_monthly_member=is_monthly_member,
                          is_yearly_member=is_yearly_member,
                          logged_member=logged_member,
                          x_ratelimit_remaining=x_ratelimit_remaining,
                          x_ratelimit=x_ratelimit,
                          x_limit_pct=x_limit_pct,
                          categories=l_categories,
                          attributes=l_attributes,
                          )
        )


class AttributeNameView(TemplateView):
    """
    Index view, displays list of attributes
    """
    template_name = 'attributes/by_name.html'

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

        attribute_name = kwargs['p_attribute_slug']

        # Common for all members views ===================================================
        l_categories = Category.objects.all()
        l_attributes = Attribute.objects.all()
        try:
            logged_member = Member.objects.get(django_user__username=request.user)
            show_describe_button = logged_member.is_editor(request)
            is_monthly_member = logged_member.is_monthly_member()
            is_yearly_member = logged_member.is_yearly_member()
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

        try:
            l_attribute = Attribute.objects.get(slug=attribute_name)
        except ObjectDoesNotExist:
            l_attribute = None
        except:
            raise

        l_inspiring_users_belongs_to_attribute = \
            InspiringUserBelongsToAttribute.objects.filter(attribute=l_attribute)
        #l_inspiring_users = InspiringUser.objects.filter(id=l_inspiring_users_belongs_to_attribute.instagram_user.id)

        return render(request,
                      self.template_name,
                      dict(
                          inspiring_users=l_inspiring_users_belongs_to_attribute,
                          l_attribute=l_attribute,

                          is_monthly_member=is_monthly_member,
                          is_yearly_member=is_yearly_member,
                          logged_member=logged_member,
                          x_ratelimit_remaining=x_ratelimit_remaining,
                          x_ratelimit=x_ratelimit,
                          x_limit_pct=x_limit_pct,
                          categories=l_categories,
                          attributes=l_attributes,
        )
        )