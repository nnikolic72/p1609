from django.contrib import admin
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
from libs.instagram.tools import InstagramUserAdminUtils

from models import InspiringUser, InspiringUserRaw, Follower, Following

# Register your models here.
class InspiringUserAdmin(admin.ModelAdmin):
    '''Definition of Admin interface for GoodUsers model'''

    def process_inspiringuser(self, request, queryset):
        '''Action -> Do what is needed to process a GoodUser with Instagram API
           Process only users that are marked to be processed -> to_be_processed==True
        '''

        instagram_utils = InstagramUserAdminUtils()
        buf = instagram_utils.process_instagram_user(request, queryset)


        self.message_user(request, buf)
    process_inspiringuser.short_description = 'Process Inspiring User by Instagram API'


    def set_inspiringusers_process_true(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected GoodUsers to True.
           Process only GoodUsers that have flag to_be_processed set to False.
           to_be_processed==False
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_false(request, queryset)
        self.message_user(request, message)
    set_inspiringusers_process_true.short_description = 'Set "To Be Processed for basic info" to "Yes"'


    def set_inspiringusers_process_false(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected GoodUsers to False.
           Process only GoodUsers that have flag to_be_processed set to True.
           to_be_processed==True
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_true(request, queryset)
        self.message_user(request, message)
    set_inspiringusers_process_false.short_description = 'Set "To Be Processed for basic info" to "No"'




    def set_inspiringusers_process_photos_true(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected GoodUsers to True.
           Process only GoodUsers that have flag to_be_processed set to False.
           to_be_processed==False
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_photos_true(request, queryset)
        self.message_user(request, message)
    set_inspiringusers_process_photos_true.short_description = 'Set "To Be Processed for photos" to "Yes"'


    def set_inspiringusers_process_photos_false(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected GoodUsers to False.
           Process only GoodUsers that have flag to_be_processed set to True.
           to_be_processed==True
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_photos_false(request, queryset)
        self.message_user(request, message)
    set_inspiringusers_process_photos_false.short_description = 'Set "To Be Processed for photos" to "No"'



    def set_inspiringusers_process_friends_true(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected GoodUsers to True.
           Process only GoodUsers that have flag to_be_processed set to False.
           to_be_processed==False
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_friends_true(request, queryset)
        self.message_user(request, message)
    set_inspiringusers_process_friends_true.short_description = 'Set "To Be Processed for Friends" to "Yes"'


    def set_inspiringusers_process_friends_false(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected GoodUsers to False.
           Process only GoodUsers that have flag to_be_processed set to True.
           to_be_processed==True
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_friends_false(request, queryset)
        self.message_user(request, message)
    set_inspiringusers_process_friends_false.short_description = 'Set "To Be Processed for Friends" to "No"'



    def set_inspiringusers_process_followings_true(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected GoodUsers to True.
           Process only GoodUsers that have flag to_be_processed set to False.
           to_be_processed==False
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_friends_true(request, queryset)
        self.message_user(request, message)
    set_inspiringusers_process_followings_true.short_description = 'Set "To Be Processed for Friends" to "Yes"'


    def set_inspiringusers_process_followings_false(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected GoodUsers to False.
           Process only GoodUsers that have flag to_be_processed set to True.
           to_be_processed==True
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_friends_false(request, queryset)
        self.message_user(request, message)
    set_inspiringusers_process_followings_false.short_description = 'Set "To Be Processed for Friends" to "No"'



    '''Determine what is displayed when GoodUser is displayed as a list'''
    list_display = ('instagram_user_name',
                    'number_of_followers',
                    'creation_date',
                    'to_be_processed_for_basic_info',
                    'to_be_processed_for_friends',
                    'to_be_processed_for_followings',
                    'to_be_processed_for_photos',
                    'pk'
    )

    '''Which fields are editable in Admin list view'''
    list_editable = (
        'to_be_processed_for_basic_info',
        'to_be_processed_for_friends',
        'to_be_processed_for_followings',
        'to_be_processed_for_photos',
    )
    '''Add fields by which you want to sort a model'''
    ordering = ('instagram_user_name',)

    #prepopulated_fields = {"instagram_user_name": ("user_name",)}

    '''Add fields from the model by which we want to filter list'''
    list_filter = ('to_be_processed_for_basic_info',
                   'to_be_processed_for_friends',
                   'to_be_processed_for_followings',
                   'to_be_processed_for_photos',
                   'instagram_user_name_valid',
                   'creation_date',

    )

    '''Add a field from the model by which you want to search'''
    search_fields = ('instagram_user_name', )

    readonly_fields = ('user_type',
    )

    '''Define a list of actions listed in Admin interface Action combo box'''
    actions = (process_inspiringuser, set_inspiringusers_process_true,
               set_inspiringusers_process_false,
               set_inspiringusers_process_photos_false,
               set_inspiringusers_process_photos_true,
               set_inspiringusers_process_friends_false,
               set_inspiringusers_process_friends_true,
               set_inspiringusers_process_followings_false,
               set_inspiringusers_process_followings_true,
    )


    '''Determine what is dispalayed on GoodUser Admin Edit form'''
    fieldsets = [
        ('General Information', {'fields': ['instagram_user_name', 'user_type',
                                            'email',

                                            ]
        }
        ),
        ('GoodUser Processing Information', {'fields': ['last_processed_for_basic_info_date',
                                                        'times_processed_for_basic_info',
                                                        'to_be_processed_for_basic_info',

                                                        'last_processed_for_friends_date',
                                                        'times_processed_for_friends',
                                                        'to_be_processed_for_friends',

                                                        'last_processed_for_followings_date',
                                                        'times_processed_for_followings',
                                                        'to_be_processed_for_followings',

                                                        'last_processed_for_photos_date',
                                                        'times_processed_for_photos',
                                                        'to_be_processed_for_photos'
        ]
        }
        ),
        ('Instagram Information', {'fields': ['number_of_media',
                                              'number_of_followers', 'number_of_followings',
                                              'instagram_user_full_name', 'instagram_profile_picture_URL',
                                              'instagram_user_bio', 'instagram_user_website_URL',
                                              'instagram_user_id', 'instagram_user_name_valid']
        }
        ),


        ('Additional Social Media Information', {'fields': ['twitter_handle', 'facebook_handle',
                                                            'eyeem_handle'
        ],
                                                 'classes': ['collapse']
        }
        ),
        ('Other Web Sites Links for Inspiring User', {'fields': ['instagram_user_profile_page_URL',
                                                                 'iconosquare_user_profile_page_URL'
        ]
        }
        ),

        #('Time Information', {'fields': ['creation_date', 'last_update_date']})
    ]


class InspiringUserRawAdmin(admin.ModelAdmin):
    '''Definition of Admin interface for GoodUsers model'''

    list_display = ('instagram_user_name', 'to_be_processed',
                    'instagram_user_name_valid', 'creation_date',
                    'last_update_date'
    )

    '''Add fields from the model by which we want to filter list'''
    list_filter = ('to_be_processed', 'instagram_user_name_valid',
                   'instagram_user_name_valid', 'creation_date',
    )

    '''Add a field from the model by which you want to search'''
    search_fields = ('instagram_user_name', )



    fieldsets = [
        ('General Information', {'fields': [
            'instagram_user_name',
            ]
        }
        ),
        ('GoodUser Processing Information', {'fields': [
            'to_be_processed'
        ]
        }
        ),


        ('Categories and Attributes', {'fields': ['category1', 'category2',
                                                  'category3', 'category4',
                                                  'category5',
                                                  'attribute_black_and_white',
                                                  'attribute_color',
                                                  'attribute_hdr',
                                                  'attribute_minimal',
                                                  'attribute_abstract',
                                                  'attribute_heavy_edit',
                                                  'attribute_macro',
                                                  'attribute_retro',
                                                  'attribute_color_splash'
        ]
        }
        ),
        ]


class FollowingAdmin(admin.ModelAdmin):
    '''Definition of Admin interface for Following model'''


    def process_following(self, request, queryset):
        '''Action -> Do what is needed to process a Following with Instagram API
           Process only Following that are marked to be processed -> to_be_processed==True
        '''

        instagram_utils = InstagramUserAdminUtils()
        buf = instagram_utils.process_instagram_user(request, queryset)

        self.message_user(request, buf)
    process_following.short_description = 'Process Following by Instagram API'



    def set_followings_process_true(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected Followings to True.
           Process only Followings that have flag to_be_processed set to False.
           to_be_processed==False
        '''

        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_true(request, queryset)
        self.message_user(request, message)
    set_followings_process_true.short_description = 'Set "To Be Processed for basic info" -> Yes'


    def set_followings_process_false(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected Followings to False.
           Process only Followings that have flag to_be_processed set to True.
           to_be_processed==True
        '''

        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_false(request, queryset)
        self.message_user(request, message)
    set_followings_process_false.short_description = 'Set "To Be Processed for basic info" -> No'








    def set_followings_process_photos_true(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected GoodUsers to True.
           Process only GoodUsers that have flag to_be_processed set to False.
           to_be_processed==False
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_photos_true(request, queryset)
        self.message_user(request, message)
    set_followings_process_photos_true.short_description = 'Set "To Be Processed for photos" to "Yes"'


    def set_followings_process_photos_false(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected GoodUsers to False.
           Process only GoodUsers that have flag to_be_processed set to True.
           to_be_processed==True
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_photos_false(request, queryset)
        self.message_user(request, message)
    set_followings_process_photos_false.short_description = 'Set "To Be Processed for photos" to "No"'



    def set_followings_process_friends_true(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected GoodUsers to True.
           Process only GoodUsers that have flag to_be_processed set to False.
           to_be_processed==False
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_friends_true(request, queryset)
        self.message_user(request, message)
    set_followings_process_friends_true.short_description = 'Set "To Be Processed for Friends" to "Yes"'


    def set_followings_process_friends_false(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected GoodUsers to False.
           Process only GoodUsers that have flag to_be_processed set to True.
           to_be_processed==True
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_friends_false(request, queryset)
        self.message_user(request, message)
    set_followings_process_friends_false.short_description = 'Set "To Be Processed for Friends" to "No"'



    def set_followings_process_followings_true(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected GoodUsers to True.
           Process only GoodUsers that have flag to_be_processed set to False.
           to_be_processed==False
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_friends_true(request, queryset)
        self.message_user(request, message)
    set_followings_process_followings_true.short_description = 'Set "To Be Processed for Friends" to "Yes"'


    def set_followings_process_followings_false(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected GoodUsers to False.
           Process only GoodUsers that have flag to_be_processed set to True.
           to_be_processed==True
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_friends_false(request, queryset)
        self.message_user(request, message)
    set_followings_process_followings_false.short_description = 'Set "To Be Processed for Friends" to "No"'


    list_display = (
        'instagram_user_name',
        'is_user_active',
        'followed_by_n_goodusers',
        'number_of_media',
        'number_of_followers', 'number_of_followings',
        'to_be_processed_for_basic_info', 'to_be_processed_for_photos'
    )

    list_editable = (
        'to_be_processed_for_basic_info', 'to_be_processed_for_photos'
    )

    ordering = ('instagram_user_name', 'instagram_user_name', 'is_user_active', )

    list_filter = ('to_be_processed_for_basic_info',
                   'to_be_processed_for_followings',
                   'to_be_processed_for_photos',
                   'instagram_user_name_valid',
                   'creation_date',
    )

    search_fields = ('instagram_user_name', )

    readonly_fields = ('user_type', 'followed_by_n_goodusers',)

    actions = (process_following,
               set_followings_process_true,
               set_followings_process_false,
               set_followings_process_photos_false,
               set_followings_process_photos_true,
    )

    fieldsets = [
        ('General Information', {'fields': [ 'instagram_user_name', 'user_type'
        ]
        }
        ),

        ('Source', {'fields': [ 'inspiringuser', 'member'
        ]
        }
        ),
        ('Followings Processing Information', {'fields': ['last_processed_for_basic_info_date',
                                                          'times_processed_for_basic_info',
                                                          'to_be_processed_for_basic_info',

                                                          'last_processed_for_photos_date',
                                                          'times_processed_for_photos',
                                                          'to_be_processed_for_photos'
        ]
        }
        ),
        ('Instagram Information', {'fields': ['number_of_media',
                                              'number_of_followers', 'number_of_followings',
                                              'instagram_user_full_name', 'instagram_profile_picture_URL',
                                              'instagram_user_bio', 'instagram_user_website_URL',
                                              'instagram_user_id', 'instagram_user_name_valid']
        }
        ),
        ]


class FollowerAdmin(admin.ModelAdmin):
    '''Definition of Admin interface for Friend model'''


    def process_friend(self, request, queryset):
        '''Action -> Do what is needed to process a Friend with Instagram API
           Process only Friends that are marked to be processed -> to_be_processed==True
        '''

        instagram_utils = InstagramUserAdminUtils()
        buf = instagram_utils.process_instagram_user(request, queryset)

        self.message_user(request, buf)
    process_friend.short_description = 'Process Follower by Instagram API'



    def set_friends_process_true(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected Friends to True.
           Process only Friends that have flag to_be_processed set to False.
           to_be_processed==False
        '''

        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_true(request, queryset)
        self.message_user(request, message)
    set_friends_process_true.short_description = 'Set "To Be Processed for basic info" -> Yes'


    def set_friends_process_false(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected Friends to False.
           Process only Friends that have flag to_be_processed set to True.
           to_be_processed==True
        '''

        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_false(request, queryset)
        self.message_user(request, message)
    set_friends_process_false.short_description = 'Set "To Be Processed for basic info" -> No'






    def set_friends_process_photos_true(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected GoodUsers to True.
           Process only GoodUsers that have flag to_be_processed set to False.
           to_be_processed==False
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_photos_true(request, queryset)
        self.message_user(request, message)
    set_friends_process_photos_true.short_description = 'Set "To Be Processed for photos" to "Yes"'


    def set_friends_process_photos_false(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected GoodUsers to False.
           Process only GoodUsers that have flag to_be_processed set to True.
           to_be_processed==True
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_photos_false(request, queryset)
        self.message_user(request, message)
    set_friends_process_photos_false.short_description = 'Set "To Be Processed for photos" to "No"'



    def set_friends_process_friends_true(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected GoodUsers to True.
           Process only GoodUsers that have flag to_be_processed set to False.
           to_be_processed==False
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_friends_true(request, queryset)
        self.message_user(request, message)
    set_friends_process_friends_true.short_description = 'Set "To Be Processed for Friends" to "Yes"'


    def set_friends_process_friends_false(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected GoodUsers to False.
           Process only GoodUsers that have flag to_be_processed set to True.
           to_be_processed==True
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_friends_false(request, queryset)
        self.message_user(request, message)
    set_friends_process_friends_false.short_description = 'Set "To Be Processed for Friends" to "No"'



    def set_friends_process_followings_true(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected GoodUsers to True.
           Process only GoodUsers that have flag to_be_processed set to False.
           to_be_processed==False
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_friends_true(request, queryset)
        self.message_user(request, message)
    set_friends_process_followings_true.short_description = 'Set "To Be Processed for Friends" to "Yes"'


    def set_friends_process_followings_false(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected GoodUsers to False.
           Process only GoodUsers that have flag to_be_processed set to True.
           to_be_processed==True
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_friends_false(request, queryset)
        self.message_user(request, message)
    set_friends_process_followings_false.short_description = 'Set "To Be Processed for Friends" to "No"'



    list_display = (
                    'instagram_user_name', 'is_user_active', 'number_of_media',
                     'number_of_followers', 'number_of_followings',
                     'to_be_processed_for_basic_info', 'to_be_processed_for_photos'
                    )

    list_editable = (
                     'to_be_processed_for_basic_info', 'to_be_processed_for_photos'
                     )

    ordering = ('instagram_user_name', 'instagram_user_name', 'is_user_active', )

    list_filter = ('to_be_processed_for_basic_info',
                   'to_be_processed_for_followings',
                   'to_be_processed_for_photos',
                    'instagram_user_name_valid',
                    'creation_date',
                   )

    search_fields = ('instagram_user_name', )

    readonly_fields = ('user_type',)

    actions = (process_friend,
               set_friends_process_true,
               set_friends_process_false,
               set_friends_process_photos_false,
               set_friends_process_photos_true,
               )

    fieldsets = [
        ('General Information', {'fields': [ 'instagram_user_name', 'user_type'
                                            ]
                                 }
         ),

        ('Source', {'fields': [ 'inspiringuser', 'member'
                               ]
                    }
         ),
        ('Friend Processing Information', {'fields': ['last_processed_for_basic_info_date',
                                                        'times_processed_for_basic_info',
                                                        'to_be_processed_for_basic_info',

                                                        'last_processed_for_photos_date',
                                                        'times_processed_for_photos',
                                                        'to_be_processed_for_photos'
                                                        ]
                                             }
         ),
        ('Instagram Information', {'fields': ['number_of_media',
                                              'number_of_followers', 'number_of_followings',
                                              'instagram_user_full_name', 'instagram_profile_picture_URL',
                                              'instagram_user_bio', 'instagram_user_website_URL',
                                              'instagram_user_id', 'instagram_user_name_valid']
                                   }
         ),
        ]

admin.site.register(Follower, FollowerAdmin)
admin.site.register(Following, FollowingAdmin)
admin.site.register(InspiringUser, InspiringUserAdmin)
admin.site.register(InspiringUserRaw, InspiringUserRawAdmin)