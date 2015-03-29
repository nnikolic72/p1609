from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
__author__ = 'tanja'

from .views import SmartFeedIndexView

urlpatterns = patterns('',
                       url(r'^$', login_required(SmartFeedIndexView.as_view()),
                           name='index'
                       ),
                       )