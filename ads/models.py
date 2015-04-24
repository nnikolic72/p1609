from __future__ import division
from django.db import models
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist


# Create your models here.


class Advertisement(models.Model):
    """
    Class to define data model of Ads master data
    """

    # for copy/paste ads
    ad_identification = models.CharField(max_length=50, null=True, blank=True,
                             verbose_name=_('Ad ID'), help_text=_('Ad ID')
    )

    ad_full_code = models.CharField(max_length=1000, null=True, blank=True,
                                    verbose_name=_('Ad Full Code'), help_text=_('Ad Full Code')
    )

    # For ads that we build from parts
    ad_partial_title = models.CharField(max_length=255, null=True, blank=True,
                                        verbose_name=_('Ad Title'), help_text=_('Ad Title')
    )

    ad_partial_photo_url = models.CharField(max_length=255, null=True, blank=True,
                                            verbose_name=_('Ad Photo URL'), help_text=_('Ad Photo URL')
    )

    ad_partial_destination_url = models.URLField(max_length=255, null=True,
                                                 blank=True, default='',
                                                 verbose_name=_('URL Ad Destination'),
                                                 help_text=_('URL Ad Destination')
    )

    ad_partial_text = models.CharField(max_length=1000, null=True, blank=True,
                                       verbose_name=_('Ad Text'), help_text=_('Ad Text')
    )

    def __unicode__(self):
        return self.ad_identification

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.creation_date = timezone.now()
        self.last_update_date = timezone.now()
        return super(Advertisement, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Ad')
        verbose_name_plural = _('Ads')
        get_latest_by = 'creation_date'
        ordering = ('ad_identification',)


class AdInstance(models.Model):
    """
    Class to define ad instances
    """

    # which ad we display
    advertisement = models.ForeignKey('ads.Advertisement', null=False, blank=False)

    # on which page we display the ad
    page_id = models.CharField(max_length=1000, null=True, blank=True,
                               verbose_name=_('Page ID'), help_text=_('Page ID')
    )

    clicks = models.IntegerField(default=0, null=False, blank=False)

    no_of_displays = models.IntegerField(default=0, null=False, blank=False)

    def __unicode__(self):
        return self.advertisement.ad_identification + ' ' + self.page_id

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.creation_date = timezone.now()
        self.last_update_date = timezone.now()
        return super(AdInstance, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Ad Instance')
        verbose_name_plural = _('Ad Instances')
        get_latest_by = 'creation_date'
        ordering = ('advertisement',)