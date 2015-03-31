from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
__author__ = 'tanja'

from .views import SmartFeedIndexView, SmartFeedConfigureView

urlpatterns = patterns('',
                       url(r'^$', login_required(SmartFeedIndexView.as_view()),
                           name='index'
                       ),
                       url(r'^configure/$', login_required(SmartFeedConfigureView.as_view()),
                           name='configure'
                       ),
                       )