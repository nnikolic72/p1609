from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
__author__ = 'n.nikolic'

from .views import (AddInspiringUserView,
    AddInspiringUserByNameView,
    InspiringUserIndexView,
    InspiringUserNameView,
    UsersBestPhotosView
)

urlpatterns = patterns('',
                       url(r'^add/$', AddInspiringUserView.as_view(),
                           name='addinspiring'
                           ),
                       url(r'^add/(?P<p_username>[_a-zA-Z\d\.]+)/$', AddInspiringUserByNameView.as_view(),
                           name='addinspiringname'
                           ),

                       url(r'^$', InspiringUserIndexView.as_view(),
                           name='index_inspiring_artists'
                       ),

                       url(r'^recent-best/(?P<p_inspiring_user_name>[_a-zA-Z\d\.]+)/$', InspiringUserNameView.as_view(),
                           name='inspiring_user'
                       ),

                       url(r'^all-time-best/(?P<p_mode>[a-z]+)/(?P<p_username>[_a-zA-Z\d\.]+)/$',
                           UsersBestPhotosView.as_view(),
                           name='alltimebest'
                           ),
                       )
