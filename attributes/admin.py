from django.contrib import admin
from django.utils.text import slugify
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

# Register your models here.
from .models import Attribute, AttributeRaw


# Register your models here.
class AttributeAdmin(admin.ModelAdmin):
    '''Definition of Admin interface for Attribute model'''


    prepopulated_fields = {"slug": ("title",)}

    # actions = (process_imported_categories,)

    list_display = ('title', 'slug',)

    ordering = ('title',)


    fieldsets = [
                ('Attribute information', { 'fields': ['title', 'description',
                                                      'slug'
                                                      ]
                                          }
                 ),
                 ]


class AttributeRawResource(resources.ModelResource):

    class Meta:
        model = AttributeRaw
        fields = ('id', 'title', 'description')
        import_id_fields = ['id']


class AttributeRawAdmin(ImportExportModelAdmin):
    '''Definition of Admin interface for Attribute model'''

    def process_raw_attributes(self, request, queryset):
        '''Action -> Create categories from imported categories CSV'''
        l_counter_update = 0
        l_counter_new = 0
        l_counter_skipped = 0
        l_errors = 0

        for attribute in queryset:
            l_process = True
            raw_category_title_slug = slugify(attribute.title)
            try:
                l_attribute = Attribute.objects.get(slug=raw_category_title_slug)
            except ObjectDoesNotExist:
                l_attribute = None
            except MultipleObjectsReturned:
                l_process = False

            if l_process:
                if l_attribute:
                    # Category exists, update it
                    l_attribute.title = attribute.title
                    l_attribute.description = attribute.description
                    try:
                        l_attribute.save()
                        l_counter_update += 1
                    except:
                        l_errors += 1

                else:
                    # this is new category
                    l_attribute_new = Attribute(title=attribute.title,
                                              slug=slugify(attribute.title),
                                              description=attribute.description)
                    try:
                        l_attribute_new.save()
                        l_counter_new += 1
                    except:
                        l_errors += 1
            else:
                l_counter_skipped += 1

        buf = "%s new attributes, %s updated attributes. Total %s processed. %s skipped. %s errors." % \
              (l_counter_new, l_counter_update, l_counter_update + l_counter_new, l_counter_skipped, l_errors)
        self.message_user(request, buf)
    process_raw_attributes.short_description = 'Process RAW imported attributes'

    actions = ('process_raw_attributes',)

    resource_class = AttributeRawResource

    list_display = ('title', 'description',
    )

    ordering = ('title',)

    fieldsets = [
        ('Attribute information', { 'fields': ['title', 'description',

                                               ]
        }
        ),
        ]



admin.site.register(Attribute, AttributeAdmin)
admin.site.register(AttributeRaw, AttributeRawAdmin)