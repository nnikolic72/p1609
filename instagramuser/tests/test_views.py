from django.contrib.auth.models import User
from django.test import TestCase
from django.core.urlresolvers import reverse
from instagramuser.models import InspiringUser
from members.models import Member

__author__ = 'n.nikolic'


class InspiringUserViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        Member.objects.create(user_type='member', django_user=self.user)
        InspiringUser.objects.get_or_create(instagram_user_id='ABCD123',
                                    instagram_user_name='pera'
                                    )

    def test_addinspiring(self):
        self.client.login(username='john', password='johnpassword')
        logged_member = Member.objects.get(user_type='member', django_user=self.user)
        response = self.client.get(reverse('instagramuser:addinspiring'), {'logged_member': logged_member})
        self.assertEqual(response.status_code, 200)

