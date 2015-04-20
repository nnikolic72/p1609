__author__ = 'n.nikolic'
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, permission_required

from .views import (
    MemberWelcomeView,
    MemberDashboardView,
    MemberDisabledView,
    MemberLogoutView,
    MemberMyAccountView,
    MemberNewMembershipView,
    MemberNewMembershipResultView,
    MemberNewFriendsResponseView,
    CommenterIndexView,
    MemberNewMonthlyMembershipView,
    MemberNewYearlyMembershipView,
)


urlpatterns = patterns('',
    url(r'^welcome/$', login_required(MemberWelcomeView.as_view()), name='welcome'),
    url(r'^dashboard/$', login_required(MemberDashboardView.as_view()), name='dashboard'),
    url(r'^disabled/$', MemberDisabledView.as_view(), name='disabled'),
    url(r'^logout/$', login_required(MemberLogoutView.as_view()), name='logout'),
    url(r'^account/$', login_required(MemberMyAccountView.as_view()), name='my_account'),
    url(r'^commenter/$', login_required(CommenterIndexView.as_view()), name='commenter_index'),
    url(r'^new-membership/$', login_required(MemberNewMembershipView.as_view()), name='new_membership'),
    url(r'^new-monthly-membership/$', login_required(MemberNewMonthlyMembershipView.as_view()), name='new_monthly_membership'),
    url(r'^new-yearly-membership/$', login_required(MemberNewYearlyMembershipView.as_view()), name='new_yearly_membership'),
    url(r'^new-membership-result/$', login_required(MemberNewMembershipResultView.as_view()), name='new_membership_result'),
    url(r'^new-membership-cancel/$', login_required(MemberNewMembershipResultView.as_view()), name='new_membership_cancel'),
    url(r'^new-friends-response/$', login_required(MemberNewFriendsResponseView.as_view()), name='new_friends_response'),
)