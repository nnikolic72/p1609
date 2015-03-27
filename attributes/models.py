from django.db import models
from django.utils.translation import ugettext as _


# Create your models here.
class Attribute(models.Model):
    '''Provide category functionality'''

    def __unicode__(self):
        '''return text for this class'''

        return(self.title)

    title = models.CharField(max_length=200, null=False, blank=False, default='')
    description = models.CharField(max_length=500, null=True, blank=True, default='')
    slug = models.SlugField(max_length=50, null=True, blank=True, default='')

    class Meta:
        ordering = ('title', )
        verbose_name = _('Attribute')
        verbose_name_plural = _('Attributes')


class AttributeRaw(models.Model):
    '''Provide category functionality'''

    def __unicode__(self):
        '''return text for this class'''

        return(self.title)


    title = models.CharField(max_length=200, null=False, blank=False, default='')
    description = models.CharField(max_length=500, null=True, blank=True, default='')


    class Meta:
        ordering = ('title', )
        verbose_name = _('Raw Attribute')
        verbose_name_plural = _('Raw Attributes')
