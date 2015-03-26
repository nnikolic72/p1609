from django.db import models
from django.utils.translation import ugettext as _


# Create your models here.
class Category(models.Model):
    '''Provide category functionality'''

    def __str__(self):
        '''return text for this class'''

        return(self.title)

    title = models.CharField(max_length=200, null=False, blank=False, default='')
    description = models.CharField(max_length=500, null=True, blank=True, default='')
    slug = models.SlugField(max_length=50, null=True, blank=True, default='')
    parent = models.ForeignKey('self', null=True, blank=True, default=None)
    app = models.CharField(max_length=20, null=True, blank=True, default='')

    class Meta:
        ordering = ('app', 'parent__title', 'title',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class CategoryRaw(models.Model):
    '''Provide category CVS import functionality'''

    title = models.CharField(max_length=200, null=False, blank=False, default='')
    description = models.CharField(max_length=500, null=True, blank=True, default='')


    class Meta:
        ordering = ('title',)
        verbose_name = _('Raw Category')
        verbose_name_plural = _('Raw Categories')