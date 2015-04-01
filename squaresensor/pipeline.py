'''
Created on Mar 5, 2015

@author: n.nikolic
'''
from django.http import Http404

from members.models import Member

def add_member(*args, **kwargs):
    '''Part of social auth pipeline - add new member'''
    
    l_is_new = kwargs[u'is_new']  # @UnusedVariable
    l_user = kwargs[u'user']
    l_backend = kwargs[u'backend']
    l_response = kwargs[u'response']
    l_response_code = l_response[u'meta'][u'code']
    if l_response_code != 200:
        raise Http404
    
    l_username = kwargs[u'username']
    l_instagram_user_id = kwargs[u'uid']
    
    l_backend_name = l_backend.name  # @UnusedVariable
    
    #if l_is_new:
    '''This is a new user - make them a new member of Squaresensor!'''
    # But first check if we have this member!
    l_check_member = Member.objects.filter(instagram_user_name=l_username)
    
    if l_check_member.count() == 0:
        '''There is no member with this username - create one'''
        l_new_member = Member(instagram_user_name=l_username, 
                              instagram_user_id=l_instagram_user_id,
                              django_user=l_user
                              )
        l_new_member.to_be_processed_for_basic_info = True
        l_new_member.to_be_processed_for_photos = True
        l_new_member.save()

        
    #profile = user.get_profile()
    