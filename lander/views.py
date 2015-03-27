from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import translation
from django.utils.translation import ugettext as _
from django.views.generic import FormView
from django.views.generic.base import TemplateView

from squaresensor.settings.base import IS_APP_LIVE

from .forms import SignUpForm
from .models import Lander


class AjaxTemplateMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'ajax_template_name'):
            split = self.template_name.split('.html')
            split[-1] = '_inner'
            split.append('.html')
            self.ajax_template_name = ''.join(split)
        if request.is_ajax():
            self.template_name = self.ajax_template_name
        return super(AjaxTemplateMixin, self).dispatch(request, *args, **kwargs)


class LanderHomePageView2(SuccessMessageMixin, AjaxTemplateMixin, FormView):
    template_name = 'lander/index.html'
    form_class = SignUpForm
    success_url = reverse_lazy('lander:signupemail')
    success_message = "Way to go!"

    def get(self, request, *args, **kwargs):
        """
        Serve GET request
        """
        x=1
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('members:dashboard'))
        else:
            return render(request, self.template_name,
                          dict(form=SignUpForm(),
                               is_app_live=IS_APP_LIVE,

                               )
            )


# Create your views here.
class LanderHomePageView(TemplateView):
    ''' Home page of lander app
    '''

    template_name = 'lander/index.html'

    def get(self, request, *args, **kwargs):
        """
        Serve GET request
        """
        x=1
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('members:dashboard'))
        else:
            return render(request, self.template_name,
                          dict(form=SignUpForm(),
                               is_app_live=IS_APP_LIVE,

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