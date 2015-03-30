from django.conf.urls import patterns, include, url
from django.contrib import admin
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponseRedirect

from squaresensor.settings.base import STATIC_URL

dajaxice_autodiscover()

urlpatterns = patterns('',
    url(r'^i18n/', include('django.conf.urls.i18n')),  # go to /i18n/setlang/
    url(r'^favicon.ico/$', lambda x: HttpResponseRedirect(STATIC_URL+'ico/favicon.ico')), #google chrome favicon fix

    url(r'^admin1609/', include(admin.site.urls)),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'', include('social_auth.urls')),
    url(r'^emoji/', include('emoji.urls')),

    url(r'^', include('lander.urls', namespace='lander')),
    url(r'^members/', include('members.urls', namespace='members')),
    url(r'^photos/', include('photos.urls', namespace='photos')),
    url(r'^categories/', include('categories.urls', namespace='categories')),
    url(r'^attributes/', include('attributes.urls', namespace='attributes')),
    url(r'^hashtags/', include('hashtags.urls', namespace='hashtags')),
    url(r'^smart-feed/', include('smartfeed.urls', namespace='smartfeed')),
    url(r'^instagramuser/', include('instagramuser.urls', namespace='instagramuser')),

)

urlpatterns += staticfiles_urlpatterns()