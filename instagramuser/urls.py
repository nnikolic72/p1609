from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
__author__ = 'n.nikolic'

from .views import AddInspiringUserView, AddInspiringUserByNameView

urlpatterns = patterns('',
                       url(r'^add/$', AddInspiringUserView.as_view(),
                           name='addinspiring'
                           ),
                       url(r'^add/(?P<p_username>.+)/$', AddInspiringUserByNameView.as_view(),
                           name='addinspiringname'
                           ),
                       )
