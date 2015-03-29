from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from categories.views import CategoryIndexView, CategoryNameView

__author__ = 'n.nikolic'

urlpatterns = patterns('',
                       url(r'^$', login_required(CategoryIndexView.as_view()),
                           name='index'
                       ),
                       url(r'^(?P<p_category_slug>.+)/$', login_required(CategoryNameView.as_view()),
                           name='category_slug'
                       ),
                       )