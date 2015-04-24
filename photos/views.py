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

from attributes.models import Attribute
from categories.models import Category

from libs.instagram.tools import InstagramSession, BestPhotos, InstagramUserAdminUtils

from .models import Photo


from instagramuser.models import Follower, Following, InspiringUser
from members.models import Member


# Create your views here.

