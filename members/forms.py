from django.forms import TextInput
from django.utils.translation import ugettext as _
from django import forms
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_forms.bootstrap import StrictButton

from .models import Membership
__author__ = 'n.nikolic'


class MembershipForm(forms.Form):
    """
    Email sing-up form for lander page
    """
    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = False # don't render form DOM element
        helper.render_unmentioned_fields = True # render all fields
        helper.label_class = 'col-md-2'
        helper.field_class = 'col-md-10'
        return helper


    FREE = 'FRE'
    PROFESSIONAL = 'PRO'
    PREMIUM = 'PRM'

    MEMBERSHIP_CHOICES = (
        (FREE, 'Free'),
        (PROFESSIONAL, 'Professional'),
        (PREMIUM, 'Premium'),
    )

    MONTHLY = 'MON'
    YEARLY = 'YEA'


    MEMBERSHIP_DURATION_CHOICES = (
        (MONTHLY, 'One Month'),
        (YEARLY, 'One Year'),
    )

    membership_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control',

                                                                        }),
                                        required=True,
                                        choices=MEMBERSHIP_CHOICES,
                                        )
    recurring_membership = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-control',

                                                                               }),
                                              required=False,
                                              )

    membership_duration = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control',
                                                                        }),
                                        required=True,
                                        choices=MEMBERSHIP_DURATION_CHOICES,
                                        )

    class Meta:
        #model = Membership
        fields = ('membership_type', 'recurring_membership', 'membership_duration')