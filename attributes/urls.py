from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from attributes.views import AttributeIndexView, AttributeNameView

__author__ = 'n.nikolic'

urlpatterns = patterns('',
                       url(r'^$', login_required(AttributeIndexView.as_view()),
                           name='index'
                       ),
                       url(r'^(?P<p_attribute_slug>.+)/$', login_required(AttributeNameView.as_view()),
                           name='attribute_slug'
                       ),
                       )