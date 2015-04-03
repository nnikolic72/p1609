from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
__author__ = 'tanja'

from .views import SmartFeedIndexView, SmartFeedConfigureView, SmartFeedConfigureCalendarView

urlpatterns = patterns('',
                       url(r'^$', login_required(SmartFeedIndexView.as_view()),
                           name='index'
                       ),
                       url(r'^configure/$', login_required(SmartFeedConfigureView.as_view()),
                           name='configure'
                       ),
                       url(r'^calendar/(?P<p_period>(\d+))d$', login_required(SmartFeedConfigureCalendarView.as_view()),
                           name='calendar'
                       ),
                       )