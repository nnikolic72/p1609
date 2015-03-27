__author__ = 'n.nikolic'
from django.conf.urls import patterns, url

from .views import (
    LanderHomePageView2, LanderSignUpView
)
__author__ = 'n.nikolic'

urlpatterns = patterns('',
    url(r'signup/$', LanderSignUpView.as_view(), name='signupemail'),
    url(r'^$', LanderHomePageView2.as_view(), name='index'),

)