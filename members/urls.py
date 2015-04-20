from datetime import timedelta
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datetime_safe import datetime
from paypal.standard.ipn.signals import valid_ipn_received, payment_was_flagged
from paypal.standard.models import ST_PP_COMPLETED
from members.models import PaymentLog, Invoice, Membership

__author__ = 'n.nikolic'
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, permission_required

from .views import (
    MemberWelcomeView,
    MemberDashboardView,
    MemberDisabledView,
    MemberLogoutView,
    MemberMyAccountView,
    MemberNewMembershipView,
    MemberNewMembershipResultView,
    MemberNewFriendsResponseView,
    CommenterIndexView,
    MemberNewMonthlyMembershipView,
    MemberNewYearlyMembershipView,
)


urlpatterns = patterns('',
                       url(r'^welcome/$', login_required(MemberWelcomeView.as_view()), name='welcome'),
                       url(r'^dashboard/$', login_required(MemberDashboardView.as_view()), name='dashboard'),
                       url(r'^disabled/$', MemberDisabledView.as_view(), name='disabled'),
                       url(r'^logout/$', login_required(MemberLogoutView.as_view()), name='logout'),
                       url(r'^account/$', login_required(MemberMyAccountView.as_view()), name='my_account'),
                       url(r'^responder/$', login_required(CommenterIndexView.as_view()), name='commenter_index'),
                       url(r'^new-membership/$', login_required(MemberNewMembershipView.as_view()), name='new_membership'),
                       url(r'^new-monthly-membership/$', login_required(MemberNewMonthlyMembershipView.as_view()), name='new_monthly_membership'),
                       url(r'^new-yearly-membership/$', login_required(MemberNewYearlyMembershipView.as_view()), name='new_yearly_membership'),
                       url(r'^new-membership-result/$', login_required(MemberNewMembershipResultView.as_view()), name='new_membership_result'),
                       url(r'^new-membership-cancel/$', login_required(MemberNewMembershipResultView.as_view()), name='new_membership_cancel'),
                       url(r'^new-friends-response/$', login_required(MemberNewFriendsResponseView.as_view()), name='new_friends_response'),
                       )


def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj:
        l_message = 'Payment response received. Status (%s). Sender (%s)' % (ipn_obj.payment_status, sender)
        l_new_payment_log = PaymentLog(invoice_number=ipn_obj.invoice,
                                       message=l_message)
    else:
        l_message = 'sender is blank'
        l_new_payment_log = PaymentLog(invoice_number=None,
                                       message=l_message)

    #l_new_payment_log = PaymentLog(invoice_number=ipn_obj.invoice,
    #                               message=l_message)
    l_new_payment_log.save()

    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # Undertake some action depending upon `ipn_obj`.

        try:
            paid_invoice = Invoice.objects.get(invoice_number=ipn_obj.invoice)
            paid_invoice.invoice_status = "paid"
            paid_invoice.save()
        except ObjectDoesNotExist:
            paid_invoice = None
        except:
            raise

        if paid_invoice:
            l_membership_start_time = datetime.today()
            l_membership_end_time = None
            if paid_invoice.membership_type == 'MON':
                l_membership_end_time = l_membership_start_time + timedelta(days=31)
            if paid_invoice.membership_type == 'PRO':
                l_membership_end_time = l_membership_start_time + timedelta(days=365)

            new_membership = Membership(membership_type=paid_invoice.membership_type,
                                        invoice=paid_invoice,
                                        member=paid_invoice.member,
                                        active_membership=True,
                                        membership_start_time=l_membership_start_time,
                                        membership_end_time=l_membership_end_time)
            new_membership.save()
            logging.debug('Paid invoice %s' % (ipn_obj.invoice))
        else:
            logging.exception('Paid invoice not found %s' % (ipn_obj.invoice))
            raise
    else:
        pass
        # something went wrong

def show_me_the_money_flagged(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj:
        l_message = 'Flagged Payment response received. Status (%s). Sender (%s)' % (ipn_obj.payment_status, sender)
        l_new_payment_log = PaymentLog(invoice_number=ipn_obj.invoice,
                                       message=l_message)
    else:
        l_message = 'Flagged. sender is blank'
        l_new_payment_log = PaymentLog(invoice_number=None,
                                       message=l_message)
    #l_new_payment_log = PaymentLog(invoice_number=ipn_obj.invoice,
    #                               message=l_message)
    l_new_payment_log.save()

    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # Undertake some action depending upon `ipn_obj`.

        try:
            paid_invoice = Invoice.objects.get(invoice_number=ipn_obj.invoice)
            paid_invoice.invoice_status = "paid"
            paid_invoice.save()
        except ObjectDoesNotExist:
            paid_invoice = None
        except:
            raise

        if paid_invoice:
            l_membership_start_time = datetime.today()
            l_membership_end_time = None

            try:
                if paid_invoice.membership_type == 'MON':
                    l_membership_end_time = l_membership_start_time + timedelta(days=31)
                if paid_invoice.membership_type == 'PRO':
                    l_membership_end_time = l_membership_start_time + timedelta(days=365)
            except:
                logging.exception('Date conversion failed %s' % (ipn_obj.invoice))
                raise

            new_membership = Membership(membership_type=paid_invoice.membership_type,
                                        invoice=paid_invoice,
                                        member=paid_invoice.member,
                                        active_membership=True,
                                        membership_start_time=l_membership_start_time,
                                        membership_end_time=l_membership_end_time)
            new_membership.save()
            logging.debug('Paid invoice %s' % (ipn_obj.invoice))
        else:
            logging.exception('Paid invoice not found %s' % (ipn_obj.invoice))
            raise
    else:
        pass
        # something went wrong

payment_was_flagged.connect(show_me_the_money_flagged)