from django.contrib import admin

# Register your models here.
from libs.instagram.tools import InstagramUserAdminUtils

from .models import SquareFollowing

class CategorySquareFollowingInlineAdmin(admin.TabularInline):
    model = SquareFollowing.categories.through


class AttributeSquareFollowingInlineAdmin(admin.TabularInline):
    model = SquareFollowing.attributes.through

class SquareFollowingMemberInlineAdmin(admin.TabularInline):
    model = SquareFollowing.member_id2.through

class SquareFollowingAdmin(admin.ModelAdmin):
    '''Definition of Admin interface for Friend model'''


    def process_friend(self, request, queryset):
        '''Action -> Do what is needed to process a Friend with Instagram API
           Process only Friends that are marked to be processed -> to_be_processed==True
        '''

        instagram_utils = InstagramUserAdminUtils()
        buf = instagram_utils.process_instagram_user(queryset)

        self.message_user(request, buf)
    process_friend.short_description = 'Process SquareFollowing by Instagram API'



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

    inlines = (CategorySquareFollowingInlineAdmin,
               AttributeSquareFollowingInlineAdmin,
               SquareFollowingMemberInlineAdmin,
    )

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

        ('Square Following Processing Information', {'fields': ['last_processed_for_basic_info_date',
                                                      'times_processed_for_basic_info',
                                                      'to_be_processed_for_basic_info',

                                                      'last_processed_for_photos_date',
                                                      'times_processed_for_photos',
                                                      'to_be_processed_for_photos'
        ]
        }
        ),
        ('Instagram Information', {'fields': ['number_of_media',
                                              'number_of_followings',
                                              'instagram_user_full_name', 'instagram_profile_picture_URL',
                                              'instagram_user_bio', 'instagram_user_website_URL',
                                              'instagram_user_id', 'instagram_user_name_valid']
        }
        ),
        ]

admin.site.register(SquareFollowing, SquareFollowingAdmin)