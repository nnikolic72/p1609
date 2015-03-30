from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from .views import HashtagIndexView, HashtagNameView

__author__ = 'n.nikolic'

urlpatterns = patterns('',
                       url(r'^$', login_required(HashtagIndexView.as_view()),
                           name='index'
                       ),
                       url(r'^(?P<p_hashtag_name>.+)/$', login_required(HashtagNameView.as_view()),
                           name='hashtag_name'
                       ),
                       )