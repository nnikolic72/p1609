from django.conf import settings
from django.contrib import admin
from django.utils import timezone
from libs.instagram.tools import InstagramSession

from .models import Photo
# Register your models here.
class PhotoAdmin(admin.ModelAdmin):
    '''Photos model Admin definition'''


    def get_instagram_photo_info(self, api, p_photo):
        '''Retrieves information about on Instagram photo

        Parameters:
        api - Instagram session object
        p_photo - source Photo object
        Returns - object filled with Instagram photo information
        '''

        l_photo = api.get_instagram_photo_info(p_photo.instagram_photo_id)

        if l_photo:
            p_photo.instagram_photo_valid = True
            p_photo.instagram_photo_id = l_photo.id
            p_photo.instagram_low_resolution_URL = \
                l_photo.get_low_resolution_url()
            p_photo.instagram_thumbnail_URL = l_photo.get_thumbnail_url()
            p_photo.instagram_standard_resolution_URL = \
                l_photo.get_standard_resolution_url()
            p_photo.instagram_link_URL = l_photo.link
            #l_cleaned_caption = self.cleanup_instagram_caption_text(l_photo.caption)
            try:
                p_photo.instagram_caption = l_photo.caption.text
            except:
                # no caption on the photo
                p_photo.instagram_caption = None
            #p_photo.instagram_tags = ','.join(l_photo.tags)
            p_photo.instagram_created_time = l_photo.created_time
            p_photo.instagram_likes = l_photo.like_count
            p_photo.instagram_comments = l_photo.comment_count
        else:
            p_photo.instagram_photo_valid = False

        return p_photo


    def process_photos_by_instagram_api(self, request, queryset):
        '''Action -> process photos by Instagram API'''

        ig_session = InstagramSession(p_is_admin=True, p_token='')
        ig_session.init_instagram_API()

        self.l_instagram_api_limit_start, self.l_instagram_api_limit = \
            ig_session.get_api_limits()

        l_counter = 0

        for obj in queryset:
            l_instagram_api_limit_current, foo = ig_session.get_api_limits()  # @UnusedVariable
            if l_instagram_api_limit_current >= settings.INSTAGRAM_API_THRESHOLD:
                obj = self.get_instagram_photo_info(ig_session, obj)
                obj.instagram_photo_processed = True
                obj.last_processed_date = timezone.datetime.now()
                obj.save()
                l_counter += 1


        self.l_instagram_api_limit_end, self.l_instagram_api_limit = \
            ig_session.get_api_limits()

        if l_counter == 1:
            buf = '1 photo processed successfully. Instagram API (%s - %s/%s / diff: %s)' % \
                  (self.l_instagram_api_limit_start, self.l_instagram_api_limit_end,
                   self.l_instagram_api_limit, (int(self.l_instagram_api_limit_start) - int(self.l_instagram_api_limit_end))
                  )
        else:
            buf = '%s photos processed successfully.  Instagram API (%s - %s/%s / diff: %s)' % \
                  (l_counter, self.l_instagram_api_limit_start, self.l_instagram_api_limit_end,
                   self.l_instagram_api_limit, (int(self.l_instagram_api_limit_start) - int(self.l_instagram_api_limit_end))
                  )
        self.message_user(request, buf)
    process_photos_by_instagram_api.short_description = 'Process photos by Instagram API'

    list_display = ('instagram_photo_id', 'inspiring_user_id', 'friend_id',
                    'following_id', 'member_id',
                    'photo_rating', 'admin_thumbnail',
                    'instagram_photo_processed',
    )

    list_filter = ('instagram_photo_processed',

                   'inspiring_user_id',
                   'friend_id',
                   'member_id',
                   'following_id',
    )

    ordering = ('inspiring_user_id', '-photo_rating', )

    '''Search by foreign key example!'''
    search_fields = ('inspiring_user_id__instagram_user_name',
    )

    filter_horizontal = ('photo_category', 'photo_attribute', )
    readonly_fields = ('admin_thumbnail',)

    fieldsets = [
        ('General Information', {'fields': ['instagram_photo_id',
                                            'inspiring_user_id',
                                            'friend_id',
                                            'member_id',
                                            'following_id',
                                            'instagram_caption',
                                            'instagram_tags',
                                            'instagram_photo_valid',
                                            'photo_rating'
        ]
        }
        ),
        ('Instagram Stats', {'fields': ['instagram_likes', 'instagram_comments'
        ]
        }
        ),
        ( 'Photo URLS', {'fields': ['instagram_low_resolution_URL', 'instagram_thumbnail_URL',
                                                   'instagram_standard_resolution_URL',
                                                   'instagram_link_URL'
        ]
        }
        ),
        ( 'Categories and Attributes', {'fields': ['admin_thumbnail', 'photo_category',
                                                   'photo_attribute'
        ]
        }
        ),

        ('Date and time information', {'fields': ['instagram_created_time'
        ]
        }
        )
    ]

    actions = (process_photos_by_instagram_api, )

admin.site.register(Photo, PhotoAdmin)