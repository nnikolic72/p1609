from django.db import models
from django.utils.datetime_safe import datetime
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from social_auth.db.django_models import UserSocialAuth

from instagramuser.models import InstagramUser
# Create your models here.
from libs.instagram.tools import InstagramSession


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

    user_type = models.CharField(editable=False, default='member', max_length=50)

    django_user = models.OneToOneField(User, null=False, blank=False,
                                       verbose_name=_('Django user'),
                                       help_text=_('Django user')
    )

    likes_in_last_minute = models.IntegerField(null=True, blank=True, default=0,
                                               verbose_name=_('Likes in LM'),
                                               help_text=_('How many likes user has given in last minute')
    )
    comments_in_last_minute = models.IntegerField(null=True, blank=True, default=0,
                                                  verbose_name=_('Comments in LM'),
                                                  help_text=_('How many comments user has given in last minute')
    )

    membership = models.ManyToManyField('members.Membership', blank=True, null=True,
                                        verbose_name=_('Membership type'),
                                        help_text=_('Membership type')
    )

    ig_api_limit_max = models.IntegerField(null=True, blank=True, default=0,
                                                  verbose_name=_('IG API Limit Max'),
                                                  help_text=_('How many IG requests are available per period')
    )

    ig_api_limit_remaining = models.IntegerField(null=True, blank=True, default=0,
                                                  verbose_name=_('IG API Limit Used'),
                                                  help_text=_('How many IG requests are remaining for period')
    )



    class Meta(InstagramUser.Meta):
        ordering = ('django_user__username',)
        verbose_name = _('Member')
        verbose_name_plural = _('Members')


class Membership(models.Model):
    """
    Model to hold membership information
    """

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

    creation_date = models.DateTimeField(editable=False)
    last_update_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.creation_date = datetime.today()
        self.last_update_date = datetime.today()
        return super(Membership, self).save(*args, **kwargs)