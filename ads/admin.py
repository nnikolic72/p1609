from django.contrib import admin

from .models import Advertisement, AdInstance


# Register your models here.
class AdvertisementAdmin(admin.ModelAdmin):

    list_display = ('ad_identification', 'ad_partial_title', 'ad_partial_destination_url',
    )

    fieldsets = [
        ('General Information', {'fields': ['ad_identification',
                                            'ad_full_code',
                                            'ad_partial_title',
                                            'ad_partial_photo_url',
                                            'ad_partial_destination_url',
                                            'ad_partial_text',

        ]
        }
        ),
        ]


class AdInstanceAdmin(admin.ModelAdmin):

    list_display = ('advertisement', 'page_id', 'no_of_displays', 'clicks',
    )

    fieldsets = [
        ('General Information', {'fields': ['advertisement', 'page_id', 'no_of_displays', 'clicks',
                                            ]
        }
        ),
        ]

admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(AdInstance, AdInstanceAdmin)