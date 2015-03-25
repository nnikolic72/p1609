from django.contrib import admin

# Register your models here.
from .models import Attribute

# Register your models here.
class AttributeAdmin(admin.ModelAdmin):
    '''Definition of Admin interface for Attribute model'''

    prepopulated_fields = {"slug": ("title",)}

    # actions = (process_imported_categories,)

    list_display = ('title', 'slug',
                    )


    ordering = ('title',)


    fieldsets = [
                ('Attribute information', { 'fields': ['title', 'description',
                                                      'slug'
                                                      ]
                                          }
                 ),
                 ]



admin.site.register(Attribute, AttributeAdmin)