__author__ = 'n.nikolic'
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, permission_required

from .views import (
    MemberWelcomeView,
    MemberDashboardView,
    MemberDisabledView,
    MemberLogoutView
)


urlpatterns = patterns('',
    url(r'^welcome/$', login_required(MemberWelcomeView.as_view()), name='welcome'),
    url(r'^dashboard/$', login_required(MemberDashboardView.as_view()), name='dashboard'),
    url(r'^disabled/$', MemberDisabledView.as_view(), name='disabled'),
    url(r'^logout/$', login_required(MemberLogoutView.as_view()), name='logout'),
)