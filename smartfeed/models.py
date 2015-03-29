from django.db import models
from django.utils.datetime_safe import datetime
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist

from attributes.models import Attribute
from categories.models import Category

from instagramuser.models import InstagramUser

class SquareFollowingBelongsToCategory(models.Model):
    instagram_user = models.ForeignKey('SquareFollowing')
    category = models.ForeignKey(Category)
    frequency = models.IntegerField(default=0, null=False, blank=False)
    weight = models.DecimalField(default=0, max_digits=10, decimal_places=2)


class SquareFollowingBelongsToAttribute(models.Model):
    instagram_user = models.ForeignKey('SquareFollowing')
    attribute = models.ForeignKey(Attribute)
    frequency = models.IntegerField(default=0, null=False, blank=False)
    weight = models.DecimalField(default=0, max_digits=10, decimal_places=2)


# Create your models here.
class SquareFollowing(InstagramUser):
    """
    Class model defining a SquareFollowing - an Instagram user that Member follows through SquareSensor Smart Feed
    """

    G = 'G'
    Y = 'Y'
    R = 'O'

    SQUAREFOLLOWING_LEVEL_CHOICES = (
        (G, 'Green'),
        (Y, 'Yellow'),
        (R, 'Off'),
    )

    squarefollowing_level = models.CharField(max_length=10, choices=SQUAREFOLLOWING_LEVEL_CHOICES, default=R)

    categories = models.ManyToManyField(Category, through='SquareFollowingBelongsToCategory', null=True, blank=True)
    attributes = models.ManyToManyField(Attribute, through='SquareFollowingBelongsToAttribute', null=True, blank=True)

    user_type = models.CharField(editable=False, default='squarefollowing', max_length=50)


    class Meta:
        verbose_name = _('SquareFollowing')
        verbose_name_plural = _('SquareFollowings')