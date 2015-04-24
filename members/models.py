from django.db import models
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from social_auth.db.django_models import UserSocialAuth

from instagramuser.models import InstagramUser
# Create your models here.
from libs.instagram.tools import InstagramSession
from categories.models import Category
from attributes.models import Attribute


class MemberBelongsToCategory(models.Model):
    instagram_user = models.ForeignKey('Member')
    category = models.ForeignKey(Category)
    frequency = models.IntegerField(default=0, null=False, blank=False)
    weight = models.DecimalField(default=0, max_digits=10, decimal_places=2)


class MemberBelongsToAttribute(models.Model):
    instagram_user = models.ForeignKey('Member')
    attribute = models.ForeignKey(Attribute)
    frequency = models.IntegerField(default=0, null=False, blank=False)
    weight = models.DecimalField(default=0, max_digits=10, decimal_places=2)


class Member(InstagramUser):
    """
    Model for Squaresensor member
    Inherits Instagram user, links to Django User and implements additional columns
    """

    def get_member_token(self, request):
        """
        """
        tokens = UserSocialAuth.get_social_auth_for_user(request.user).get().tokens
        return tokens

    def refresh_api_limits(self, request):
        """
        Updates Instagram API limits
        """
        l_token = self.get_member_token(request)
        ig_session = InstagramSession(p_is_admin=False, p_token=l_token['access_token'])
        ig_session.init_instagram_API()
        x_ratelimit_remaining, x_ratelimit = ig_session.get_api_limits()

        if x_ratelimit_remaining:
            self.ig_api_limit_remaining = int(x_ratelimit_remaining)

        if x_ratelimit:
            self.ig_api_limit_max = int(x_ratelimit)

        self.save()
        return self.ig_api_limit_remaining, self.ig_api_limit_max

    def get_api_limits(self):
        """
        Returns current Instagram API limits without calling IG API
        """
        return self.ig_api_limit_remaining, self.ig_api_limit_max

    def is_editor(self, req):
        """
        Checks if member is in "Inspiring User Editor" group
        """
        l_is_editor = False
        try:
            groups_memberships = req.user.groups.all()
            describe_group = Group.objects.get(name='Inspiring User Editor')
            if describe_group in groups_memberships:
                l_is_editor = True
        except ObjectDoesNotExist:
            pass
        except:
            raise

        return l_is_editor

    def is_monthly_member(self):
        l_is_monthly_member = False
        for membership_i in Membership.objects.filter(member=self, membership_type='MON', active_membership=True):
            l_is_monthly_member = True

        return l_is_monthly_member

    def is_yearly_member(self):
        l_is_yearly_member = False
        for membership_i in Membership.objects.filter(member=self, membership_type='PRO', active_membership=True):
            l_is_yearly_member = True

        return l_is_yearly_member

    def check_membership_expired(self):
        l_active_memberships = Membership.objects.filter(member=self,
                                                         active_membership=True)
        for membership in l_active_memberships:
            if membership.membership_end_time < timezone.now():
                membership.active_membership = False
                membership.save()

    def get_active_membership(self):
        l_active_membership = None

        try:
            l_active_membership = Membership.objects.get(member=self, active_membership=True)
        except ObjectDoesNotExist:
            l_active_membership = None
        except:
            raise

        return l_active_membership

    user_type = models.CharField(editable=False, default='member', max_length=50)

    categories = models.ManyToManyField(Category, through='MemberBelongsToCategory', null=True, blank=True)
    attributes = models.ManyToManyField(Attribute, through='MemberBelongsToAttribute', null=True, blank=True)

    django_user = models.OneToOneField(User, null=False, blank=False,
                                       verbose_name=_('Django user'),
                                       help_text=_('Django user')
    )

    likes_in_last_minute = models.IntegerField(null=True, blank=True, default=0,
                                               verbose_name=_('Likes in LM'),
                                               help_text=_('How many likes user has given in last minute')
    )
    likes_in_last_minute_interval_start = models.DateTimeField(null=True, blank=True,
                                                               verbose_name=_('Likes period start'),
                                                               help_text=_('When like limit period started')
    )

    comments_in_last_minute = models.IntegerField(null=True, blank=True, default=0,
                                                  verbose_name=_('Comments in LM'),
                                                  help_text=_('How many comments user has given in last minute')
    )
    comments_in_last_minute_interval_start = models.DateTimeField(null=True, blank=True,
                                                               verbose_name=_('Comments period start'),
                                                               help_text=_('When comment limit period started')
    )

    new_friends_in_last_day = models.IntegerField(null=True, blank=True, default=0,
                                                  verbose_name=_('NewFriends in LD'),
                                                  help_text=_('How many new friends member interacted during last day')
    )
    new_friends_in_last_day_interval_start = models.DateTimeField(null=True, blank=True,
                                                               verbose_name=_('NewFriends period start'),
                                                               help_text=_('When new friends limit period started')
    )

    #membership = models.ManyToManyField('members.Membership', blank=True, null=True,
    #                                    verbose_name=_('Membership type'),
    #                                    help_text=_('Membership type')
    #)

    smartfeed_last_seen_instagram_photo_id = models.CharField(max_length=100, blank=True, null=True)

    ig_api_limit_max = models.IntegerField(null=True, blank=True, default=0,
                                           verbose_name=_('IG API Limit Max'),
                                           help_text=_('How many IG requests are available per period')
    )

    ig_api_limit_remaining = models.IntegerField(null=True, blank=True, default=0,
                                                 verbose_name=_('IG API Limit Used'),
                                                 help_text=_('How many IG requests are remaining for period')
    )

    daily_new_friends_interactions = models.IntegerField(null=True, blank=True, default=0,
                                                         verbose_name=_('Daily Interactions'),
                                                         help_text=_('How many daily interactions a member had')
    )

    daily_new_friends_interactions_date = models.DateField(null=True, blank=True
    )

    help_first_time_wizard = models.BooleanField(default=True, null=False, blank=False)
    help_first_time_wizard_cur_step = models.IntegerField(default=1, null=False, blank=False)
    help_members_dashboard = models.BooleanField(default=True, null=False, blank=False)
    help_members_commenter = models.BooleanField(default=True, null=False, blank=False)
    help_photos_modal_comment_section = models.BooleanField(default=True, null=False, blank=False)
    help_photos_allbest = models.BooleanField(default=True, null=False, blank=False)
    help_smartfeed_index = models.BooleanField(default=True, null=False, blank=False)
    help_smartfeed_configure = models.BooleanField(default=True, null=False, blank=False)
    help_instagramuser_find_new_friends = models.BooleanField(default=True, null=False, blank=False)
    help_instagramuser_index_inspiring_artists2 = models.BooleanField(default=True, null=False, blank=False)
    help_categories_index = models.BooleanField(default=True, null=False, blank=False)
    help_attributes_index = models.BooleanField(default=True, null=False, blank=False)
    help_reserved1 = models.BooleanField(default=True, null=False, blank=False)
    help_reserved2 = models.BooleanField(default=True, null=False, blank=False)
    help_reserved3 = models.BooleanField(default=True, null=False, blank=False)
    help_reserved4 = models.BooleanField(default=True, null=False, blank=False)
    help_reserved5 = models.BooleanField(default=True, null=False, blank=False)

    class Meta(InstagramUser.Meta):
        ordering = ('django_user__username',)
        verbose_name = _('Member')
        verbose_name_plural = _('Members')


class Invoice(models.Model):
    """
    Invoices for membership payments
    """
    invoice_number = models.CharField(max_length=200, null=True, blank=True,
                                       default="",
                                       verbose_name=_('Invoice number'),
                                       help_text=_('Invoice number')
    )
    membership_type = models.CharField(max_length=20, null=True, blank=True,
                                       default="",
                                       verbose_name=_('Membership Type'),
                                       help_text=_('Membership Type')
    )

    member = models.ForeignKey('members.Member', null=True, blank=True)
    invoice_status = models.CharField(max_length=20, null=True, blank=True,
                                       default="unpaid",
                                       verbose_name=_('Invoice status'),
                                       help_text=_('Invoice status')
    )


class PaymentLog(models.Model):
    invoice_number = models.CharField(max_length=200, null=True, blank=True,
                                       default="",
                                       verbose_name=_('Invoice number'),
                                       help_text=_('Invoice number')
    )

    message = models.CharField(max_length=500, null=True, blank=True,
                                       default="",
                                       verbose_name=_('Payment record'),
                                       help_text=_('Payment record')
    )

class Membership(models.Model):
    """
    Model to hold membership information
    """

    def __unicode__(self):
        return str(self.pk)

    member = models.ForeignKey('members.Member', null=True, blank=True)
    membership_type = models.CharField(max_length=200, null=False, blank=False,
                                       default="Free",
                                       verbose_name=_('Membership type'),
                                       help_text=_('Membership type')
    )
    membership_start_time = models.DateTimeField(null=True,blank=True,
                                                 verbose_name=_('Membership start time'),
                                                 help_text=_('Membership start time')
    )
    membership_end_time = models.DateTimeField(null=True,blank=True,
                                               verbose_name=_('Membership end time'),
                                               help_text=_('Membership end time')
    )

    recurring_membership = models.BooleanField(default=False, null=False, blank=False,
                                               verbose_name=_('Recurring'),
                                               help_text=_('Is membership recurring?')
    )

    active_membership = models.BooleanField(default=False, null=False, blank=False,
                                            verbose_name=_('Active'),
                                            help_text=_('Is membership active?')
    )
    #invoice_number = models.CharField(max_length=200, null=True, blank=True,
    #                                   default="",
    #                                   verbose_name=_('Invoice number'),
    #                                   help_text=_('Invoice number')
    #)

    invoice = models.ForeignKey('members.Invoice', null=True, blank=True)

    creation_date = models.DateTimeField(editable=False)
    last_update_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.creation_date = datetime.today()
        self.last_update_date = datetime.today()
        return super(Membership, self).save(*args, **kwargs)


