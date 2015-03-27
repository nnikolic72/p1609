

__author__ = 'n.nikolic'

from django.forms import TextInput
from django.utils.translation import ugettext as _
from django import forms
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_forms.bootstrap import StrictButton

from .models import Lander

class SignUpForm(ModelForm):
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


    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': _('Your name'),
                                                         }),
                           required=False,
                           )
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': _('Your valid email address'),
                                                            }),
                             required=True,
                             )

    class Meta:
        model = Lander
        fields = ('email', 'name',)