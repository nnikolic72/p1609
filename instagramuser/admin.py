from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from libs.instagram.tools import InstagramUserAdminUtils, InstagramSession

from models import InspiringUser, InspiringUserRaw, Follower, Following, NewFriendContactedByMember
from photos.models import Photo

from .tasks import process_instagram_user


class CategoryInspiringUserInlineAdmin(admin.TabularInline):
    model = InspiringUser.categories.through


class AttributeInspiringUserInlineAdmin(admin.TabularInline):
    model = InspiringUser.attributes.through


# Register your models here.
class InspiringUserAdmin(admin.ModelAdmin):
    '''Definition of Admin interface for GoodUsers model'''

    def process_inspiringuser(self, request, queryset):
        '''Action -> Do what is needed to process a GoodUser with Instagram API
           Process only users that are marked to be processed -> to_be_processed==True
        '''
        buf = 'Finished.'
        #instagram_utils = InstagramUserAdminUtils()

        inspiring_users_id_list = []
        for inspiring_user in queryset:
            inspiring_users_id_list.extend([inspiring_user.instagram_user_id])
        l_is_admin = True
        l_token = ''
        process_instagram_user.delay(None, inspiring_users_id_list, l_is_admin, l_token )

        self.message_user(request, buf)
    process_inspiringuser.short_description = 'Process Inspiring User by Instagram API'

    def check_ig_limits(self, request, queryset):
        '''Action -> Do what is needed to process a GoodUser with Instagram API
           Process only users that are marked to be processed -> to_be_processed==True
        '''
        buf = 'Finished.'
        #instagram_utils = InstagramUserAdminUtils()
        instagram_session = InstagramSession(p_is_admin=True, p_token='')
        instagram_session.init_instagram_API()
        x_ratelimit_remaining, x_ratelimit = instagram_session.get_api_limits()

        buf = 'Limit: %s, Remaining: %s' % (x_ratelimit, x_ratelimit_remaining)

        self.message_user(request, buf)
    check_ig_limits.short_description = 'Check Instagram API limits'

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

    inlines = (CategoryInspiringUserInlineAdmin, AttributeInspiringUserInlineAdmin,)

    '''Determine what is displayed when GoodUser is displayed as a list'''
    list_display = ('instagram_user_name',
                    'number_of_followers',
                    'creation_date',
                    'times_processed_for_friends',
                    'times_processed_for_followings',
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
               check_ig_limits,
    )

    '''Determine what is dispalayed on GoodUser Admin Edit form'''
    fieldsets = [
        ('General Information', {'fields': ['instagram_user_name', 'user_type',
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


class InspiringUserRawResource(resources.ModelResource):

    class Meta:
        model = InspiringUserRaw
        fields = ('id', 'instagram_user_name')
        import_id_fields = ['id']


class InspiringUserRawAdmin(ImportExportModelAdmin):
    '''Definition of Admin interface for InspiringUser model'''


    def process_raw_inspiring_users(self, request, queryset):
        '''Action -> Create Inspiring Users from imported Inspiring Users CSV'''
        l_counter_update = 0
        l_counter_new = 0
        l_counter_skipped = 0
        l_errors = 0

        instagram_session = InstagramSession(p_is_admin=True, p_token='')
        instagram_session.init_instagram_API()

        for inspiring_user in queryset:
            l_process = True
            l_inspiring_user = None

            try:
                l_inspiring_user = InspiringUser.objects.get(instagram_user_name=inspiring_user.instagram_user_name)
            except ObjectDoesNotExist:
                l_inspiring_user = None
            except MultipleObjectsReturned:
                l_process = False

            if l_process:
                if l_inspiring_user:
                    # InspiringUser exists, skip it
                    pass
                else:
                    user_search = instagram_session.is_instagram_user_valid(inspiring_user.instagram_user_name)
                    if user_search:
                        if user_search[0].username == inspiring_user.instagram_user_name:
                            instagram_user = instagram_session.get_instagram_user(user_search[0].id)
                            # this is new category
                            l_inspiring_user_new = InspiringUser(instagram_user_id=instagram_user.id)
                            l_inspiring_user_new.number_of_followers = instagram_user.counts[u'followed_by']
                            l_inspiring_user_new.number_of_followings = instagram_user.counts[u'follows']
                            l_inspiring_user_new.number_of_media = instagram_user.counts[u'media']
                            l_inspiring_user_new.instagram_user_name = instagram_user.username
                            l_inspiring_user_new.instagram_user_full_name = instagram_user.full_name
                            l_inspiring_user_new.instagram_profile_picture_URL = instagram_user.profile_picture
                            l_inspiring_user_new.instagram_user_bio = instagram_user.bio
                            l_inspiring_user_new.instagram_user_website_URL = instagram_user.website
                            l_inspiring_user_new.instagram_user_name_valid = True
                            l_inspiring_user_new.to_be_processed_for_basic_info = True
                            l_inspiring_user_new.to_be_processed_for_photos = True
                            try:
                                l_inspiring_user_new.save()
                                inspiring_user.to_be_processed = False
                                inspiring_user.instagram_user_name_valid = True
                                inspiring_user.save()
                                l_counter_new += 1

                                #process IG user and their photos
                                q = InspiringUser.objects.filter(instagram_user_name=inspiring_user.instagram_user_name)
                                if len(q) > 0:
                                    ig_admin_utils = InstagramUserAdminUtils()
                                    ig_admin_utils.process_instagram_user(q)
                                    l_photos_queryset = Photo.objects.filter(inspiring_user_id=l_inspiring_user_new)
                                    if l_photos_queryset.count() > 0:
                                        ig_admin_utils.process_photos_by_instagram_api(l_photos_queryset)
                            except:
                                l_errors += 1
                        else:
                            inspiring_user.to_be_processed = False
                            inspiring_user.instagram_user_name_valid = False
                            inspiring_user.save()

            else:
                inspiring_user.to_be_processed = False
                inspiring_user.save()
                l_counter_skipped += 1

        buf = "%s new inspiring users, %s updated inspiring users. Total %s processed. %s skipped. %s errors." % \
              (l_counter_new, l_counter_update, l_counter_update + l_counter_new, l_counter_skipped, l_errors)
        self.message_user(request, buf)
    process_raw_inspiring_users.short_description = 'Process RAW imported Inspiring Users'

    actions = ('process_raw_inspiring_users', )

    resource_class = InspiringUserRawResource

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


class CategoryFollowingInlineAdmin(admin.TabularInline):
    model = Following.categories.through


class AttributeFollowingInlineAdmin(admin.TabularInline):
    model = Following.attributes.through


class FollowingAdmin(admin.ModelAdmin):
    '''Definition of Admin interface for Following model'''


    def process_following(self, request, queryset):
        '''Action -> Do what is needed to process a Following with Instagram API
           Process only Following that are marked to be processed -> to_be_processed==True
        '''

        instagram_utils = InstagramUserAdminUtils()
        buf = instagram_utils.process_instagram_user(queryset)

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

    inlines = (CategoryFollowingInlineAdmin, AttributeFollowingInlineAdmin,)

    list_display = (
        'instagram_user_name',
        'is_user_active',
        'followed_by_n_inspiring_users',
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

    readonly_fields = ('user_type', 'followed_by_n_inspiring_users',)

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



class CategoryFollowerInlineAdmin(admin.TabularInline):
    model = Follower.categories.through


class AttributeFollowerInlineAdmin(admin.TabularInline):
    model = Follower.attributes.through


class FollowerAdmin(admin.ModelAdmin):
    '''Definition of Admin interface for Friend model'''

    def process_friend(self, request, queryset):
        '''Action -> Do what is needed to process a Friend with Instagram API
           Process only Friends that are marked to be processed -> to_be_processed==True
        '''

        instagram_utils = InstagramUserAdminUtils()
        buf = instagram_utils.process_instagram_user(queryset)

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

    inlines = (CategoryFollowerInlineAdmin, AttributeFollowerInlineAdmin,)

    list_display = (
        'instagram_user_name', 'is_user_active', 'number_of_media',
        'number_of_followers', 'number_of_followings', 'interaction_count',
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
        ('General Information', {'fields': [ 'instagram_user_name', 'user_type', 'deactivated_by_mod'
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
        ('Source', {'fields': [ 'inspiringuser', 'member', 'interaction_count'
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


class NewFriendContactedByMemberAdmin(admin.ModelAdmin):
    list_display = (
        'member', 'friend', 'contact_date',
        'response_date', 'contact_count',
        'interaction_type'
    )

    fieldsets = [
        ('General Information', {'fields': [ 'member', 'friend', 'contact_date',
                                             'response_date', 'contact_count',
                                             'interaction_type'
        ]
        }
        ),
        ]

admin.site.register(Follower, FollowerAdmin)
admin.site.register(Following, FollowingAdmin)
admin.site.register(InspiringUser, InspiringUserAdmin)
admin.site.register(InspiringUserRaw, InspiringUserRawAdmin)
admin.site.register(NewFriendContactedByMember, NewFriendContactedByMemberAdmin)