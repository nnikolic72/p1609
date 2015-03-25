from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import translation
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView

from .forms import SignUpForm
from .models import Lander

# Create your views here.
class LanderHomePageView(TemplateView):
    ''' Home page of lander app
    '''

    template_name = 'lander/index.html'

    def get(self, request, *args, **kwargs):
        """
        Serve GET request
        """

        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('members:dashboard'))
        else:
            return render(request, self.template_name,
                          dict(form=SignUpForm(),
                               )
            )

class LanderSignUpView(TemplateView):
    """ Thank you page
    """

    template_name = 'lander/signup.html'

    def post(self, request, *args, **kwargs):
        """
        Process Lander page Signup form submission request
        :param request:
        :type request:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        signup_form = SignUpForm(self.request.POST)

        if signup_form.is_valid():
            email = signup_form.cleaned_data['email']
            name = signup_form.cleaned_data['name']

            new_signup = Lander(name=name, email=email)
            new_signup.save()
            return render(request, self.template_name,
                          dict(error=False ))
        else:
            #template_name = 'lander/index.html'
            return HttpResponseRedirect(reverse('lander:index'))
            #return render(request, self.template_name,
            #              dict(request=request, error=True ))

    def get(self, request, *args, **kwargs):
        '''Serve GET request'''

        return render(request, self.template_name,
                      dict(request=request, ))