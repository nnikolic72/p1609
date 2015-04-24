__author__ = 'tanja'
from django.forms import TextInput
from django.utils.translation import ugettext as _
from django import forms
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_forms.bootstrap import StrictButton

from .models import InspiringUser

class AddInspiringUserForm(forms.Form):
    """
    Email sing-up form for lander page
    """
    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = False # don't render form DOM element
        helper.render_unmentioned_fields = True # render all fields
        helper.label_class = 'col-md-3'
        helper.field_class = 'col-md-9'
        return helper


    instagram_user_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': _('Instagram user name'),
                                                         }),
                           required=True,
                           )


    class Meta:

        fields = ('instagram_user_name',)