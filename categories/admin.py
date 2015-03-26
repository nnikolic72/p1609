from django.contrib import admin
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from import_export import resources
from import_export.admin import ImportExportModelAdmin

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


class CategoryRawResource(resources.ModelResource):

    class Meta:
        model = CategoryRaw
        fields = ('id', 'title', 'description')
        import_id_fields = ['id']


class CategoryRawAdmin(ImportExportModelAdmin):
    '''Definition of Admin interface for GoodUsers model'''
    resource_class = CategoryRawResource

    def process_raw_categories(self, request, queryset):
        '''Action -> Create categories from imported categories CSV'''
        l_counter_update = 0
        l_counter_new = 0
        l_counter_skipped = 0
        l_errors = 0

        for category in queryset:
            l_process = True
            raw_category_title_slug = slugify(category.title)
            try:
                l_category = Category.objects.get(slug=raw_category_title_slug)
            except ObjectDoesNotExist:
                l_category = None
            except MultipleObjectsReturned:
                l_process = False

            if l_process:
                if l_category:
                    # Category exists, update it
                    l_category.title = category.title
                    l_category.description = category.description
                    try:
                        l_category.save()
                        l_counter_update += 1
                    except:
                        l_errors += 1

                else:
                    # this is new category
                    l_category_new = Category(title=category.title,
                                              slug=slugify(category.title),
                                              description=category.description)
                    try:
                        l_category_new.save()
                        l_counter_new += 1
                    except:
                        l_errors += 1
            else:
                l_counter_skipped += 1

        buf = "%s new categories, %s updated categories. Total %s processed. %s skipped. %s errors." % \
              (l_counter_new, l_counter_update, l_counter_update + l_counter_new, l_counter_skipped, l_errors)
        self.message_user(request, buf)
    process_raw_categories.short_description = 'Process RAW imported categories'

    list_display = ('title', 'description',)
    ordering = ( 'title',)
    actions = ('process_raw_categories', )

    fieldsets = [
                ('Category RAW information', { 'fields': ['title',
                                                          'description'
                                                      ]
                                          }
                 ),
                 ]




admin.site.register(CategoryRaw, CategoryRawAdmin)
admin.site.register(Category, CategoryAdmin)