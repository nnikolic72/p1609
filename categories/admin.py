from django.contrib import admin

# Register your models here.
from .models import (
                     Category, CategoryRaw
                     )

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    '''Definition of Admin interface for GoodUsers model'''

    def process_imported_categories(self, request, queryset):
        '''Action -> Create categories hierarchy from imported categories CSV'''

        l_counter = 0
        l_errors = 0

        for obj in queryset:
            category_list = obj.title.split('>')

            if len(category_list) == 2:
                '''Has parent category'''
                l_parent = category_list[0].strip()
                l_child = category_list[1].strip()
                obj.title = l_child

                '''Does parent category exist?'''
                l_check_parent = Category.objects.filter(title=l_parent)
                if not l_check_parent:
                    '''We need to create Parent category first'''
                    l_errors += 1
                else:
                    obj.parent = Category.objects.get(title=l_parent)
                    obj.save()
                    l_counter += 1


        buf = "%s categories processed. %s errors - no parent category" % (l_counter, l_errors)
        self.message_user(request, buf)
    process_imported_categories.short_description = 'Process imported categories - create hierarchy'

    prepopulated_fields = {"slug": ("title",)}

    actions = (process_imported_categories,)

    list_display = ('title', 'slug', 'parent', 'app'
                    )


    ordering = ('app', 'parent__title', 'title',)

    list_filter = ('app', )

    fieldsets = [
                ('Category information', { 'fields': ['title', 'parent', 'description',
                                                      'slug', 'app'
                                                      ]
                                          }
                 ),
                 ]

'''
class CategoryResource(resources.ModelResource):

    class Meta:
        model = Category


class CategoryResourceAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    pass
'''


class CategoryRawAdmin(admin.ModelAdmin):
    '''Definition of Admin interface for GoodUsers model'''

    def process_raw_categories(self, request, queryset):
        '''Action -> Create categories hierarchy from imported categories CSV'''
        l_counter = 0
        l_errors = 0

        buf = "%s categories processed. %s errors - no parent category" % (l_counter, l_errors)
        self.message_user(request, buf)
    process_raw_categories.short_description = 'Process imported categories - create hierarchy'

    list_display = ('title', 'parent', 'description',)
    ordering = ('parent', 'title',)
    actions = ('process_raw_categories', )

    fieldsets = [
                ('Category RAW information', { 'fields': ['title', 'parent',
                                                          'description'
                                                      ]
                                          }
                 ),
                 ]

admin.site.register(CategoryRaw, CategoryRawAdmin)
admin.site.register(Category, CategoryAdmin)