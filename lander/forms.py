__author__ = 'n.nikolic'
from django.forms import TextInput
from django.utils.translation import ugettext as _
from django import forms
from django.forms import ModelForm

from .models import Lander

class SignUpForm(ModelForm):
    """
    Email sing-up form for lander page
    """
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