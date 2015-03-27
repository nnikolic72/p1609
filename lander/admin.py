from django.contrib import admin

from .models import Lander

# Register your models here.
class LanderAdmin(admin.ModelAdmin):
    list_display = ('email',
                    'name',
                    'created_at',
                    'updated_at',
    )

    """
    list_editable = ('email',
                     'name',
    )
    """

    ordering = ('email',
    )

    search_fields = ('email',
    )

    readonly_fields = ('created_at',
                       'updated_at',
    )

    fieldsets = [
        ('General Information', {'fields': [
            'email', 'name'
        ]
        }
        )
    ]


admin.site.register(Lander, LanderAdmin)