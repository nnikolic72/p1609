from django.contrib import admin
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
from libs.instagram.tools import InstagramUserAdminUtils

from squaresensor.settings.base import (INSTAGRAM_CLIENT_ID, INSTAGRAM_CLIENT_SECRET, INSTAGRAM_REDIRECT_URI,
INSTAGRAM_SECRET_KEY)

from .models import (
    Member,
    Membership
)


class CategoryInlineAdmin(admin.TabularInline):
    model = Member.categories.through

class AttributeInlineAdmin(admin.TabularInline):
    model = Member.attributes.through

class MemberAdmin(admin.ModelAdmin):
    def process_member(self, request, queryset):
        '''Action -> Do what is needed to process a Members with Instagram API
           Process only Members that are marked to be processed -> to_be_processed==True
        '''

        instagram_utils = InstagramUserAdminUtils()
        buf = instagram_utils.process_instagram_user(request, queryset)


        self.message_user(request, buf)
    process_member.short_description = 'Process Members by Instagram API'


    def set_members_process_true(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected Members to True.
           Process only Members that have flag to_be_processed set to False.
           to_be_processed==False
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_false(request, queryset)
        self.message_user(request, message)
    set_members_process_true.short_description = 'Set "To Be Processed for basic info" to "Yes"'


    def set_members_process_false(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected Members to False.
           Process only Members that have flag to_be_processed set to True.
           to_be_processed==True
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_true(request, queryset)
        self.message_user(request, message)
    set_members_process_false.short_description = 'Set "To Be Processed for basic info" to "No"'

    def set_members_process_photos_true(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected GoodUsers to True.
           Process only GoodUsers that have flag to_be_processed set to False.
           to_be_processed==False
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_photos_true(request, queryset)
        self.message_user(request, message)
    set_members_process_photos_true.short_description = 'Set "To Be Processed for photos" to "Yes"'


    def set_members_process_photos_false(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected GoodUsers to False.
           Process only GoodUsers that have flag to_be_processed set to True.
           to_be_processed==True
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_photos_false(request, queryset)
        self.message_user(request, message)
    set_members_process_photos_false.short_description = 'Set "To Be Processed for photos" to "No"'



    def set_members_process_friends_true(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected GoodUsers to True.
           Process only GoodUsers that have flag to_be_processed set to False.
           to_be_processed==False
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_friends_true(request, queryset)
        self.message_user(request, message)
    set_members_process_friends_true.short_description = 'Set "To Be Processed for Friends" to "Yes"'


    def set_members_process_friends_false(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected GoodUsers to False.
           Process only GoodUsers that have flag to_be_processed set to True.
           to_be_processed==True
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_friends_false(request, queryset)
        self.message_user(request, message)
    set_members_process_friends_false.short_description = 'Set "To Be Processed for Friends" to "No"'



    def set_members_process_followings_true(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected GoodUsers to True.
           Process only GoodUsers that have flag to_be_processed set to False.
           to_be_processed==False
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_friends_true(request, queryset)
        self.message_user(request, message)
    set_members_process_followings_true.short_description = 'Set "To Be Processed for Friends" to "Yes"'


    def set_members_process_followings_false(self, request, queryset):
        '''Action -> Set "to_be_processed" flag for selected GoodUsers to False.
           Process only GoodUsers that have flag to_be_processed set to True.
           to_be_processed==True
        '''
        admin_utils = InstagramUserAdminUtils()
        message = admin_utils.set_instagram_users_process_friends_false(request, queryset)
        self.message_user(request, message)
    set_members_process_followings_false.short_description = 'Set "To Be Processed for Friends" to "No"'

    inlines = (CategoryInlineAdmin, AttributeInlineAdmin,)

    # Register your models here.
    list_display = ('django_user', 'instagram_user_name',
                    'number_of_followers', 'creation_date',
                    'to_be_processed_for_basic_info',
                    'to_be_processed_for_friends',
                    'to_be_processed_for_followings',
                    'to_be_processed_for_photos',
                    'pk'
    )

    actions = (process_member, set_members_process_true,
               set_members_process_false,
               set_members_process_photos_false,
               set_members_process_photos_true,
               set_members_process_friends_false,
               set_members_process_friends_true,
               set_members_process_followings_false,
               set_members_process_followings_true,
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
    list_filter = (
                   'to_be_processed_for_basic_info',
                   'to_be_processed_for_friends',
                   'to_be_processed_for_followings',
                   'to_be_processed_for_photos',
                   'instagram_user_name_valid',
                   'creation_date',
    )

    '''Add a field from the model by which you want to search'''
    search_fields = ('instagram_user_name', )

    readonly_fields = ('creation_date',
                       'last_update_date',
    )

    '''Define a list of actions listed in Admin interface Action combo box'''


    #filter_horizontal = ('user_category', 'user_attribute', )

    '''Determine what is displayed on member Admin Edit form'''
    fieldsets = [
        ('General Information', {'fields': ['django_user', 'instagram_user_name',
                                            'email',

                                            ]
        }
        ),
       ('Maths', {'fields': ['poly_order',
                              'poly_theta_0',
                              'poly_theta_1',
                              'poly_theta_2',
                              'poly_theta_3',
                              'poly_theta_4',
                              'poly_min_days',
                              'poly_max_days',
                              'poly_min_likes',
                              'poly_max_likes',
        ]
        }
        ),
        ('Member Processing Information', {'fields': ['last_processed_for_basic_info_date',
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
                                              'instagram_user_id', 'instagram_user_name_valid',
                                              'smartfeed_last_seen_instagram_photo_id']
        }
        ),

        ('Additional Social Media Information', {'fields': ['twitter_handle', 'facebook_handle',
                                                            'eyeem_handle'
        ],
                                                 'classes': ['collapse']
        }
        ),
        ('Other Web Sites Links for Good User', {'fields': ['instagram_user_profile_page_URL',
                                                            'iconosquare_user_profile_page_URL'
        ]
        }
        ),

        #('Time Information', {'fields': ['creation_date', 'last_update_date']})
    ]

admin.site.register(Member, MemberAdmin)