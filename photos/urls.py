from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
__author__ = 'n.nikolic'

from .views import UsersBestPhotosView

urlpatterns = patterns('',
                       url(r'^all-time-best/(?P<p_mode>.+)/(?P<p_username>.+)/$', UsersBestPhotosView.as_view(),
                           name='alltimebest'
                           ),
                       )