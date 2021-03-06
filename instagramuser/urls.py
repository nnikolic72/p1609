from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
__author__ = 'n.nikolic'

from .views import (AddInspiringUserView,
    AddInspiringUserByNameView,
    InspiringUserIndexView,
    InspiringUserNameView,
    UsersBestPhotosView,
    AnyUserRecentBestView,
    FindFriendsView,
    InspiringUserIndexAllView,
    NewFriendsProcessingView,
    SuggestedInspiringUserIndexAllView,
    FindNewInspiringUsersView
)



urlpatterns = patterns('',
                       url(r'^add/$', login_required(AddInspiringUserView.as_view()),
                           name='addinspiring'
                           ),
                       url(r'^find-new-inspiring-artists/$', login_required(FindNewInspiringUsersView.as_view()),
                           name='find_new_inspiring_users'
                           ),
                       url(r'^new-friends/$', login_required(FindFriendsView.as_view()),
                           name='new_friends'
                           ),
                       url(r'^add/(?P<p_username>[_a-zA-Z\d\.]+)/$', login_required(AddInspiringUserByNameView.as_view()),
                           name='addinspiringname'
                           ),
                       url(r'^$', login_required(InspiringUserIndexView.as_view()),
                           name='index_inspiring_artists'
                       ),
                       url(r'^all-inspiring-artists/$', login_required(InspiringUserIndexAllView.as_view()),
                           name='index_all_inspiring_artists'
                       ),
                       url(r'^suggested-inspiring-artists/$', login_required(SuggestedInspiringUserIndexAllView.as_view()),
                           name='suggested_inspiring_artists'
                       ),
                       url(r'^new-friends-processing/$', login_required(NewFriendsProcessingView.as_view()),
                           name='new_friends_processing'
                       ),
                       url(r'^recent-best/(?P<p_inspiring_user_name>[_a-zA-Z\d\.]+)/$',
                           login_required(InspiringUserNameView.as_view()),
                           name='inspiring_user'
                       ),

                       url(r'^get-recent-best/(?P<p_instagram_user_name>[_a-zA-Z\d\.]+)/$',
                           login_required(AnyUserRecentBestView.as_view()),
                           name='any_user_recent_best'
                       ),

                       url(r'^all-time-best/(?P<p_mode>[a-z]+)/(?P<p_username>[_a-zA-Z\d\.]+)/$',
                           login_required(UsersBestPhotosView.as_view()),
                           name='alltimebest'
                           ),




                       )


