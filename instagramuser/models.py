from django.db import models
from django.utils.datetime_safe import datetime
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist


# Create your models here.
class InstagramUser(models.Model):
    """Abstract base class for Inspiring, Members, Friends and Followings"""


    def __unicode__(self):
        """return text for this class"""

        return self.instagram_user_name

    email = models.EmailField(null=True, blank=True,
                              verbose_name=_('E-Mail'), help_text=_('E-Mail address')
    )
    twitter_handle = models.CharField(max_length=100, null=True, blank=True,
                                      verbose_name=_('Twitter username'), help_text=_('Twitter username')
    )
    facebook_handle = models.CharField(max_length=100, null=True, blank=True,
                                       verbose_name=_('Facebook username'), help_text=_('Facebook username')
    )
    eyeem_handle = models.CharField(max_length=100, null=True, blank=True,
                                    verbose_name=_('EyeEm username'), help_text=_('EyeEm username')
    )
    instagram_user_name = models.CharField(max_length=100, unique=True,
                                           verbose_name=_('Instagram username'), help_text=_('Instagram username')
    )
    instagram_user_name_valid = models.BooleanField(default=True, null=False,
                                                    verbose_name=_('IG username valid'),
                                                    help_text=_('Check if Instagram user is valid/exists.')
    )
    instagram_user_id = models.CharField(max_length=100, unique=True, null=True,
                                         blank=True,
                                         verbose_name=_('Instagram user id'), help_text=_('Instagram user id')
    )
    instagram_user_profile_page_URL = models.URLField(max_length=255, null=True,
                                                      blank=True, default='',
                                                      verbose_name=_('Instagram profile URL'),
                                                      help_text=_('Instagram user profile page URL')
    )
    iconosquare_user_profile_page_URL = models.URLField(max_length=255, null=True,
                                                        blank=True, default='',
                                                        verbose_name=_('Iconosquare profile URL'),
                                                        help_text=_('Iconosquare user profile page URL')
    )
    instagram_profile_picture_URL = models.URLField(max_length=255, null=True,
                                                    blank=True,
                                                    verbose_name=_('Instagram profile page URL'),
                                                    help_text=_('Instagram profile page URL')
    )
    instagram_user_bio = models.TextField(max_length=500, null=True, blank=True,
                                          verbose_name=_('Instagram user bio'),
                                          help_text=_('Instagram user bio')
    )
    instagram_user_website_URL = models.URLField(max_length=255, null=True,
                                                 blank=True,
                                                 verbose_name=_('IG profile URL'),
                                                 help_text=_('Instagram user web site URL')
    )

    instagram_user_full_name = models.CharField(max_length=100, null=True,
                                                blank=True,
                                                verbose_name=_('IG full name'),
                                                help_text=_('Instagram user full name')
    )
    is_user_active = models.BooleanField(default=False, null=False,
                                         verbose_name=_('IG user active'),
                                         help_text=_('Is Instagram user active?')
    )

    number_of_followers = models.IntegerField(default=0, null=True, blank=True,
                                              verbose_name=_('# of followers'),
                                              help_text=_('Number of Instagram followers')
    )
    number_of_followings = models.IntegerField(default=0, null=True, blank=True,
                                               verbose_name=_('# of Followings'),
                                               help_text=_('Number of Instagram followings')
    )
    number_of_media = models.IntegerField(default=0, null=True, blank=True,
                                          verbose_name=_('# of Posts'),
                                          help_text=_('Number of Instagram posts')
    )

    '''Number of times Instagram user is processed for basic info'''
    times_processed_for_basic_info = models.IntegerField(
        _('Number of times Instagram user was processed for basic info'),
        default=0, null=False
    )
    '''Time-stamp when was the last time GoodUser was processed for Friends using Instagram API'''
    last_processed_for_basic_info_date = models.DateTimeField(
        _('Instagram user processed date for basic info'),
        null=True, blank=True
    )
    '''GoodUser is marked for processing next time GoodUser Batch Processing is run'''
    to_be_processed_for_basic_info = models.BooleanField(verbose_name=_('TBP Basic Info'), default=False, null=False,
                                                         help_text=_('Check if you want this Instagram user to be '
                                                                     'processed in the next Batch Run'
                                                         )
    )

    '''Time-stamp when was the last time Instagram user was processed for Friends using Instagram API'''
    last_processed_for_friends_date = models.DateTimeField(_('Instagram user processed for friends date'),
                                                           null=True, blank=True
    )
    '''Number of times Instagram user is processed for friends'''
    times_processed_for_friends = models.IntegerField(
        _('Number of times Instagram user was processed for friends'),
        default=0, null=False
    )
    '''GoodUser is marked for processing for friends next time Instagram user Batch Processing is run'''
    to_be_processed_for_friends = models.BooleanField(verbose_name='TBP Friends', default=False, null=False,
                                                      help_text=_('Check if you want this Instagram user to be '
                                                                  'processed for friends in the next Batch Run'
                                                      )
    )

    '''Time-stamp when was the last time Instagram user was processed for Followings using Instagram API'''
    last_processed_for_followings_date = models.DateTimeField(_('Instagram user processed for Followings date'),
                                                              null=True, blank=True
    )
    '''Number of times Instagram user is processed for friends'''
    times_processed_for_followings = models.IntegerField(
        _('Number of times Instagram user was processed for Followings'),
        default=0, null=False
    )
    '''GoodUser is marked for processing for Followings next time Instagram user Batch Processing is run'''
    to_be_processed_for_followings = models.BooleanField(verbose_name=_('TBP Followings'),
                                                         default=False, null=False,
                                                         help_text=_('Check if you want this Instagram user to be '
                                                                     'processed for Followings in the next Batch Run'
                                                         )
    )

    '''Time-stamp when was the last time Instagram user was processed for Photos using Instagram API'''
    last_processed_for_photos_date = models.DateTimeField(_('Instagram user processed for Photos date'),
                                                          null=True, blank=True
    )
    '''Number of times Instagram user is processed for friends'''
    times_processed_for_photos = models.IntegerField(
        _('Number of times Instagram user was processed for Photos'),
        default=0, null=False
    )
    '''GoodUser is marked for processing for Photos next time Instagram user Batch Processing is run'''
    to_be_processed_for_photos = models.BooleanField(verbose_name=_('TBP Photos'),
                                                     default=False, null=False,
                                                     help_text=_('Check if you want this Instagram user to be '
                                                                 'processed for Photos in the next Batch Run'
                                                     )
    )

    creation_date = models.DateTimeField(editable=False)
    last_update_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.creation_date = datetime.today()
        self.last_update_date = datetime.today()
        return super(InstagramUser, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        get_latest_by = 'creation_date'
        ordering = ('instagram_user_name',)


class InspiringUser(InstagramUser):
    """
    Model to hold inspiring user data
    """

    user_type = models.CharField(editable=False, default='inspiring', max_length=50)
    is_potential_friend = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        verbose_name = _('Inspiring User')
        verbose_name_plural = _('Inspiring Users')


class InspiringUserRaw(models.Model):
    '''Class for import of CSV data. Import a text file into this model and run Action
       "Process RAW data to GoodUser
    '''

    def __str__(self):
        '''return text for this class'''

        return(self.instagram_user_name)

    instagram_user_name = models.CharField(max_length=100, null=False, blank=False)
    category1 = models.CharField(max_length=100, null=True, blank=True)
    category2 = models.CharField(max_length=100, null=True, blank=True)
    category3 = models.CharField(max_length=100, null=True, blank=True)
    category4 = models.CharField(max_length=100, null=True, blank=True)
    category5 = models.CharField(max_length=100, null=True, blank=True)
    attribute_black_and_white = models.CharField(max_length=100, null=True, blank=True)
    attribute_color = models.CharField(max_length=100, null=True, blank=True)
    attribute_hdr = models.CharField(max_length=100, null=True, blank=True)
    attribute_minimal = models.CharField(max_length=100, null=True, blank=True)
    attribute_abstract = models.CharField(max_length=100, null=True, blank=True)
    attribute_heavy_edit = models.CharField(max_length=100, null=True, blank=True)
    attribute_macro = models.CharField(max_length=100, null=True, blank=True)
    attribute_retro = models.CharField(max_length=100, null=True, blank=True)
    attribute_color_splash = models.CharField(max_length=100, null=True, blank=True)

    instagram_user_name_valid = models.BooleanField(default=True, null=False,
                                          help_text=_('Check if Instagram user is valid/exists.')
                                          )
    to_be_processed = models.BooleanField(default=True, null=False,
                                          help_text=_('Check if you want this Good User to be '
                                                     'processed in the next Batch Run'
                                                     )
                                          )
    creation_date = models.DateTimeField('InspiringUserRaw creation date', auto_now_add=True)
    last_update_date = models.DateTimeField('InspiringUserRaw creation date', auto_now=True)

    class Meta:
        get_latest_by = 'creation_date'
        ordering = ('instagram_user_name',)
        verbose_name = 'Inspiring User Raw'
        verbose_name_plural = 'Inspiring Users Raw'


class Follower(InstagramUser):
    """

    """
    user_type = models.CharField(editable=False, default='follower', max_length=50)
    is_potential_friend = models.BooleanField(default=False, null=False, blank=False)
    inspiringuser = models.ManyToManyField('instagramuser.InspiringUser', null=True, blank=True)
    member = models.ManyToManyField('members.Member', null=True, blank=True)

    class Meta:
        verbose_name = _('Follower')
        verbose_name_plural = _('Followers')


class Following(InstagramUser):
    """

    """
    user_type = models.CharField(editable=False, default='following', max_length=50)
    is_potential_friend = models.BooleanField(default=False, null=False, blank=False)
    def followed_by_n_goodusers(self):
        '''How many goodusers follow this Following'''
        gooduser_count = self.inspiringuser.count()

        return gooduser_count
    #followed_by_n_goodusers.admin_order_field = 'gooduser__count'
    #followed_by_n_goodusers.boolean = True
    followed_by_n_goodusers.short_description = '# of GoodUsers'

    inspiringuser = models.ManyToManyField('instagramuser.InspiringUser', null=True, blank=True)
    member = models.ManyToManyField('members.Member', null=True, blank=True)

    class Meta:
        verbose_name = _('Following')
        verbose_name_plural = _('Followings')

